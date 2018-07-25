import rapid7vmconsole
import csv
from StringIO import StringIO
import json
import base64
from time import sleep


def generate_report():
    config = rapid7vmconsole.Configuration(name='Rapid7')
    #There is no OAuth. We know this is dumb. For demo purposes
    config.username = '<insert field>'
    config.password = '<insert field>'
    config.host = '<insert field>'
    config.verify_ssl = False
    config.assert_hostname = False
    config.proxy = None
    config.ssl_ca_cert = None
    config.connection_pool_maxsize = None
    config.cert_file = None
    config.key_file = None
    config.safe_chars_for_path_param = ''

    auth = "%s:%s" % (config.username, config.password)
    auth = base64.b64encode(auth.encode('ascii')).decode()
    client = rapid7vmconsole.ApiClient(configuration=config)
    client.default_headers['Authorization'] = "Basic %s" % auth
    report_client = rapid7vmconsole.ReportApi(client)

    report_id = create_report_sql(report_client, 'vulnReport', '''
    select da.asset_id, da.mac_address, da.ip_address, das.port, dv.vulnerability_id, 
        dv.title, dv.description, dv.severity, dv.cvss_score, dv.exploits, dv.nexpose_id
    from fact_asset_vulnerability_finding as fpr 
    join dim_vulnerability as dv on fpr.vulnerability_id = dv.vulnerability_id 
    join dim_asset as da on fpr.asset_id = da.asset_id 
    join dim_asset_service as das on fpr.asset_id = das.asset_id''')

    #print(report_id)

    report_instance_id = run_report(report_client, report_id)
    #print(report_instance_id)

    report = download_report(report_client, report_id, report_instance_id)
    with open('nexpose_vul_report1.txt', 'w') as f:
        f.write(report)

    reader = csv.DictReader(StringIO(report))
    reader.next()
    critical_vulns = []

    for row in reader:
        try:
            if float(row['cvss_score']) > 9.5 and int(row['exploits']) >= 1:
                critical_vulns.append(row)
        except Exception as e:
            print(e)
    """with open('test', 'w') as a:
        vulnCount = 0
        for row in reader:
            try:
                if float(row['cvss_score']) > 9.5 and int(row['exploits']) >= 1:
                    a.write(json.dumps(row, indent=4))
                    vulnCount += 1
            except Exception as e:
                print(e)
        print(vulnCount) """

    delete_report(report_client, report_id)
    return critical_vulns


def create_report_sql(client, report_name, sql):
    report_config = rapid7vmconsole.Report(name=report_name, format='sql-query', query=sql, version='2.3.0')
    response = client.create_report(report=report_config)
    return response.id


def run_report(client, report_id):
    report = client.generate_report(report_id)
    return report.id


def download_report(client, report_id, instance_id):
    report_done = False

    while not report_done:
        report_instance_status = client.get_report_instance(report_id, instance_id).status

        if any(report_instance_status in s for s in ['aborted', 'failed', 'complete']):
            report_done = True

            report_contents = client.download_report(report_id, instance_id)

            return report_contents
        else:
            sleep(30)


def delete_report(client, report_id):
    client.delete_report(report_id)



if __name__ == '__main__':
    generate_report()
