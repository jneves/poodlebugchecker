# -*- coding: utf-8 -*-
import os
import codecs

def vulnerable(host, port=443):
    r = os.system("nmap --script ssl-enum-ciphers -p %d %s | grep 'SSLv3: No supported ciphers found' > /dev/null" % (port, host))
    if not r:
        return False
    r = os.system("nmap --script ssl-enum-ciphers -p %d %s | grep 'SSLv3' > /dev/null" % (port, host))
    if not r:
        return True
    return False

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
]

pt_state_list = [
    'www.seg-social.pt',
    'www.portaldasfinancas.gov.pt',
    'dri2.seg-social.pt',
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
        output += u"""<div class="ink-alert basic %s" role="alert">
                        <i class="fa fa-times"></i> %s - <b>%s</b>
                      </div>""" % (css_class, key, u"Vulnerável" if value else u"Não vulnerável")
    f = codecs.open('index.html', 'w', 'utf-8')
    t1 = codecs.open('template1.html', 'r', 'utf-8').read()
    t2 = codecs.open('template2.html', 'r', 'utf-8').read()
    f.write(t1)
    f.write(output)
    f.write(t2)
