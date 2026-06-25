import os
import ssl
import socket
import datetime
import json
import requests
import urllib3
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_KEY = os.environ.get("AUDIT_API_KEY", "")

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Content-Type-Options",
    "X-Frame-Options",
    "X-XSS-Protection",
    "Referrer-Policy",
    "Permissions-Policy",
]

SENSITIVE_KEYWORDS = [
    "password", "passwd", "secret", "token", "api_key", "apikey",
    "access_key", "private_key", "auth", "credential", "ssn", "credit_card",
]

ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]


def authenticate(target_url):
    headers = {}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
        print(f"[AUTH] Usando API Key para autenticacion.")
    else:
        print("[AUTH] No se encontro AUDIT_API_KEY. Continuando sin autenticacion.")
    return headers


def check_security_headers(target_url, auth_headers):
    print(f"\n[HEADERS] Verificando cabeceras HTTP de seguridad en: {target_url}")
    results = {}
    try:
        response = requests.get(target_url, headers=auth_headers, timeout=10, verify=False)
        for header in SECURITY_HEADERS:
            present = header in response.headers
            value = response.headers.get(header, "NO PRESENTE")
            results[header] = {"present": present, "value": value}
            status = "OK" if present else "FALTA"
            print(f"  [{status}] {header}: {value}")
    except requests.RequestException as e:
        print(f"  [ERROR] No se pudo conectar: {e}")
    return results


def check_http_methods(target_url, auth_headers):
    print(f"\n[METODOS] Verificando metodos HTTP habilitados en: {target_url}")
    enabled = []
    disabled = []
    for method in ALLOWED_METHODS:
        try:
            response = requests.request(
                method, target_url, headers=auth_headers, timeout=8, verify=False
            )
            if response.status_code not in [405, 501]:
                enabled.append((method, response.status_code))
                print(f"  [HABILITADO] {method} -> HTTP {response.status_code}")
            else:
                disabled.append((method, response.status_code))
                print(f"  [DESHABILITADO] {method} -> HTTP {response.status_code}")
        except requests.RequestException:
            disabled.append((method, "Error"))
    return {"enabled": enabled, "disabled": disabled}


def check_sensitive_exposure(target_url, auth_headers):
    print(f"\n[SENSIBLE] Verificando exposicion de informacion sensible en: {target_url}")
    findings = []
    try:
        response = requests.get(target_url, headers=auth_headers, timeout=10, verify=False)
        body_lower = response.text.lower()
        for keyword in SENSITIVE_KEYWORDS:
            if keyword in body_lower:
                findings.append(keyword)
                print(f"  [ALERTA] Posible exposicion de '{keyword}' en la respuesta")
        if not findings:
            print("  [OK] No se detecto informacion sensible en la respuesta.")
    except requests.RequestException as e:
        print(f"  [ERROR] No se pudo verificar: {e}")
    return findings


def check_ssl(hostname, port=443):
    print(f"\n[SSL] Validando certificado SSL de: {hostname}:{port}")
    result = {"valid": False, "expiry": None, "issuer": None, "subject": None, "error": None}
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
            s.settimeout(8)
            s.connect((hostname, port))
            cert = s.getpeercert()

        not_after = cert.get("notAfter", "")
        expiry_dt = datetime.datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
        days_left = (expiry_dt - datetime.datetime.utcnow()).days

        issuer = dict(x[0] for x in cert.get("issuer", []))
        subject = dict(x[0] for x in cert.get("subject", []))

        result["valid"] = days_left > 0
        result["expiry"] = expiry_dt.strftime("%Y-%m-%d")
        result["days_left"] = days_left
        result["issuer"] = issuer.get("organizationName", "Desconocido")
        result["subject"] = subject.get("commonName", hostname)

        print(f"  [OK] Dominio: {result['subject']}")
        print(f"  [OK] Emisor: {result['issuer']}")
        print(f"  [{'OK' if days_left > 30 else 'ALERTA'}] Vence: {result['expiry']} ({days_left} dias restantes)")

    except ssl.SSLCertVerificationError as e:
        result["error"] = f"Certificado invalido: {e}"
        print(f"  [ERROR] {result['error']}")
    except Exception as e:
        result["error"] = str(e)
        print(f"  [ERROR] {result['error']}")

    return result


def generate_txt_report(target_url, hostname, headers_result, methods_result, sensitive_result, ssl_result, output_path):
    lines = []
    lines.append("=" * 60)
    lines.append("   REPORTE DE AUDITORIA DE SEGURIDAD PARA APIs")
    lines.append("=" * 60)
    lines.append(f"Objetivo: {target_url}")
    lines.append(f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    lines.append("--- CABECERAS HTTP DE SEGURIDAD ---")
    for h, v in headers_result.items():
        status = "OK" if v["present"] else "FALTA"
        lines.append(f"  [{status}] {h}: {v['value']}")
    lines.append("")

    lines.append("--- METODOS HTTP HABILITADOS ---")
    for m, code in methods_result.get("enabled", []):
        lines.append(f"  [HABILITADO] {m} -> {code}")
    for m, code in methods_result.get("disabled", []):
        lines.append(f"  [DESHABILITADO] {m} -> {code}")
    lines.append("")

    lines.append("--- EXPOSICION DE INFORMACION SENSIBLE ---")
    if sensitive_result:
        for kw in sensitive_result:
            lines.append(f"  [ALERTA] '{kw}' encontrado en la respuesta")
    else:
        lines.append("  [OK] No se detecto informacion sensible.")
    lines.append("")

    lines.append("--- VALIDACION SSL ---")
    if ssl_result.get("error"):
        lines.append(f"  [ERROR] {ssl_result['error']}")
    else:
        lines.append(f"  Dominio   : {ssl_result.get('subject', 'N/A')}")
        lines.append(f"  Emisor    : {ssl_result.get('issuer', 'N/A')}")
        lines.append(f"  Vencimiento: {ssl_result.get('expiry', 'N/A')} ({ssl_result.get('days_left', 0)} dias)")
        lines.append(f"  Estado    : {'VALIDO' if ssl_result.get('valid') else 'VENCIDO'}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\n[REPORTE] TXT guardado en: {output_path}")


def generate_pdf_report(target_url, hostname, headers_result, methods_result, sensitive_result, ssl_result, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            leftMargin=0.75*inch, rightMargin=0.75*inch,
                            topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("title", parent=styles["Title"], fontSize=16, spaceAfter=6)
    h2_style = ParagraphStyle("h2", parent=styles["Heading2"], fontSize=12, spaceBefore=12, spaceAfter=4)
    normal = styles["Normal"]

    story = []
    story.append(Paragraph("Reporte de Auditoria de Seguridad para APIs", title_style))
    story.append(Paragraph(f"Objetivo: {target_url}", normal))
    story.append(Paragraph(f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal))
    story.append(Spacer(1, 12))

    story.append(Paragraph("1. Cabeceras HTTP de Seguridad", h2_style))
    h_data = [["Cabecera", "Estado", "Valor"]]
    for h, v in headers_result.items():
        estado = "OK" if v["present"] else "FALTA"
        val = v["value"][:50] + "..." if len(v["value"]) > 50 else v["value"]
        h_data.append([h, estado, val])
    t = Table(h_data, colWidths=[2.4*inch, 0.8*inch, 3.3*inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.black),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))

    story.append(Paragraph("2. Metodos HTTP", h2_style))
    m_data = [["Metodo", "Estado", "Codigo HTTP"]]
    for m, c in methods_result.get("enabled", []):
        m_data.append([m, "HABILITADO", str(c)])
    for m, c in methods_result.get("disabled", []):
        m_data.append([m, "DESHABILITADO", str(c)])
    t2 = Table(m_data, colWidths=[1.5*inch, 2*inch, 2*inch])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.black),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(t2)
    story.append(Spacer(1, 8))

    story.append(Paragraph("3. Exposicion de Informacion Sensible", h2_style))
    if sensitive_result:
        for kw in sensitive_result:
            story.append(Paragraph(f"  ALERTA: '{kw}' detectado en la respuesta.", normal))
    else:
        story.append(Paragraph("  No se detecto informacion sensible en la respuesta.", normal))
    story.append(Spacer(1, 8))

    story.append(Paragraph("4. Validacion SSL", h2_style))
    if ssl_result.get("error"):
        story.append(Paragraph(f"  ERROR: {ssl_result['error']}", normal))
    else:
        ssl_data = [
            ["Dominio", ssl_result.get("subject", "N/A")],
            ["Emisor", ssl_result.get("issuer", "N/A")],
            ["Vencimiento", f"{ssl_result.get('expiry', 'N/A')} ({ssl_result.get('days_left', 0)} dias)"],
            ["Estado", "VALIDO" if ssl_result.get("valid") else "VENCIDO"],
        ]
        t3 = Table(ssl_data, colWidths=[1.8*inch, 4.7*inch])
        t3.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.lightgrey]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        story.append(t3)

    doc.build(story)
    print(f"[REPORTE] PDF guardado en: {output_path}")


def run_audit(target_url):
    from urllib.parse import urlparse
    parsed = urlparse(target_url)
    hostname = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == "https" else 80)

    print(f"\n{'='*55}")
    print(f"  AUDITOR DE SEGURIDAD PARA APIs")
    print(f"  Objetivo: {target_url}")
    print(f"{'='*55}")

    auth_headers = authenticate(target_url)
    headers_result = check_security_headers(target_url, auth_headers)
    methods_result = check_http_methods(target_url, auth_headers)
    sensitive_result = check_sensitive_exposure(target_url, auth_headers)

    ssl_result = {}
    if parsed.scheme == "https":
        ssl_result = check_ssl(hostname, port)
    else:
        print("\n[SSL] Objetivo no usa HTTPS. Omitiendo validacion SSL.")

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    txt_path = f"audit_report_{timestamp}.txt"
    pdf_path = f"audit_report_{timestamp}.pdf"

    generate_txt_report(target_url, hostname, headers_result, methods_result, sensitive_result, ssl_result, txt_path)
    generate_pdf_report(target_url, hostname, headers_result, methods_result, sensitive_result, ssl_result, pdf_path)

    print(f"\n[COMPLETADO] Auditoria finalizada.")
    return txt_path, pdf_path


if _name_ == "_main_":
    import sys
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Ingrese la URL del objetivo (ej: https://api.ejemplo.com): ").strip()
        if not url:
            url = "https://httpbin.org"

    run_audit(url)