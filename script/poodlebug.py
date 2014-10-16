# -*- coding: utf-8 -*-
import os
import codecs

def vulnerable(host, port=443):
    r = os.system("echo 'GET /\n\n' | openssl s_client -connect %s:%d -ssl3 2>&1 | grep 'DONE' > /dev/null" % (host, port))
    if r:
        return False
    return True

def sanitize_host(host):
    safe_host = host
    port = 443
    if ':' in host:
        safe_host, port = host.split(':')
        port = int(port)
    return safe_host, port

pt_bank_list = [
    'caixadirectaonline.cgd.pt',
    'net24.montepio.pt',
    'www.particulares.santandertotta.pt',
    'ind.millenniumbcp.pt',
    'bes-sec.bes.pt',
    'www.activobank.pt',
    'www.bpinet.pt',
    'www.barclays.pt',
    'www.bigonline.pt',
    'caonline.credito-agricola.pt',
    'www.be.grupobanif.pt',
    'www.bancobest.pt',
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
            if vulnerable(host, port):
                r = True
            else:
                r = False
            res.append({hostname: r})
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
                      </div>""" % (css_class, icon, key, u"Vulnerável" if value else u"Não vulnerável")
    f = codecs.open('index.html', 'w', 'utf-8')
    t1 = codecs.open('template1.html', 'r', 'utf-8').read()
    t2 = codecs.open('template2.html', 'r', 'utf-8').read()
    f.write(t1)
    f.write(output)
    f.write(t2)
