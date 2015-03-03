# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import codecs

def vulnerable(host, port=443):
    res = []
    r = os.system("echo 'GET /\n\n' | openssl s_client -connect %s:%d -ssl3 2>&1 | grep 'DONE' > /dev/null" % (host, port))
    if not r:
        res.append('POODLE')
    r = os.system("echo 'GET /\n\n' | openssl s_client -connect %s:%d -cipher EXPORT 2>&1 | grep 'DONE' > /dev/null" % (host, port))
    if not r:
        res.append('FREAK')
    return res

def sanitize_host(host):
    safe_host = host
    port = 443
    if ':' in host:
        safe_host, port = host.split(':')
        port = int(port)
    return safe_host, port

pt_bank_list = [
    # Bancos
    'www.activobank.pt',
    'emp.bancobaieuropa.pt',
    'priv.bancobaieuropa.pt',
    'www.be.grupobanif.pt',
    'homebanking.bancobic.pt',
    'www.bbva.pt',
    'connexis.bnpparibas.com',
    'www.bpinet.pt',
    'www.bpinetempresas.pt',
    'ind.millenniumbcp.pt',
    'www.bigonline.pt',
    'bes-sec.bes.pt',
    'www.bancoinvest.pt',
    'www.bancocarregosa.com',
    'www2.bancopopular.pt',
    'www.particulares.santandertotta.pt',
    'www.particulares.atlantico.eu',
    'www.bancobest.pt',
    'areareservada.caixabi.pt',
    'caixadirectaonline.cgd.pt',
    'net24.montepio.pt',
    # Crédito Agrícola
    'caonline.credito-agricola.pt',
    # Subsidiárias
    'europa.bb.com.br',
    'www.barclays.pt',
    'lu-directnet.credit-suisse.com',
    'dafbanking.deutsche-bank.pt',
    'bancaelectronica.abanca.pt',
    'zonasegura.uci.com',
    # Desconhecido
    'p24.privatbank.lv',
    # Outros serviços
    'www.mbnet.pt',
]

pt_state_list = [
    'www.seg-social.pt',
    'www.portaldasfinancas.gov.pt',
    'dri2.seg-social.pt',
    'www.viactt.pt',
]

lists = [
    pt_bank_list,
    pt_state_list
]

def generate_report():
    res = []
    for host_list in lists:
        for hostname in host_list:
            host, port = sanitize_host(hostname)
            vulns = vulnerable(host, port)
            res.append({hostname: vulns})
    return res


if __name__ == "__main__":
    res = generate_report()
    output = u''
    for d in res:
        key = d.keys()[0]
        value = d.values()[0]
        css_class = "error" if value else "success"
        icon = "fa-times" if value else "fa-check"
        output += u"""<div class="ink-alert basic %s" role="alert">
                        <i class="fa %s"></i> %s - <b>%s</b>
                      </div>""" % (css_class, icon, key, u"Vulnerável (" + u", ".join(value) + ")" if value else u"Não vulnerável")
    f = codecs.open('index.html', 'w', 'utf-8')
    t1 = codecs.open('template1.html', 'r', 'utf-8').read()
    t2 = codecs.open('template2.html', 'r', 'utf-8').read()
    f.write(t1)
    f.write(output)
    f.write(t2)
