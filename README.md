<img align = "left" src="https://i.imgur.com/g89b9Na.png">
<br><br><br><br>
A solution to improve security operations through the automation and harmonic orchestration of tools that deal with threat intelligence management, security event management, and SecOps processes. The SOAR project aims to create a centralized system to more easily access, manage, and remediate security incidents in lab endpoints, effectively decreasing incident response times while increasing the efficiency of the security/devOps process.



## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

-Python 2.7 <br>
-<a href="https://github.com/rbw0/pysnow">Pysnow Library</a><br>
-<a href="https://github.com/rapid7/vm-console-client-python/blob/master/rapid7vmconsole/rest.py">Rapid7 Nexpose Library</a><br>
-Forescout CounterAct<br>
-Rapid7 Nexpose<br>
-Service Now 

### Installing

Download Python 2.7 and install the libraries listed in the prerequisites. Make sure to have admin access and credentials to ForeScout, Rapid7 Nexpose, and ServiceNow to be able to successfully test policies, workflows, and the code. 


## The Code
<b>nexpose.py</b> - REST API that generates csv reports from the most recent Rapid7 Nexpose scans into a readable format for ServiceNow. Using the <a href="https://help.rapid7.com/nexpose/en-us/warehouse/warehouse-schema.html">Nexpose ER Diagram</a>, the SQL query below can be easily editted to add or remove additional columns of information in the final generated report.<br> 
```
report_id = create_report_sql(report_client, 'vulnReport', '''
    select da.asset_id, da.mac_address, da.ip_address, das.port, dv.vulnerability_id, 
        dv.title, dv.description, dv.severity, dv.cvss_score, dv.exploits, dv.nexpose_id
    from fact_asset_vulnerability_finding as fpr 
    join dim_vulnerability as dv on fpr.vulnerability_id = dv.vulnerability_id 
    join dim_asset as da on fpr.asset_id = da.asset_id 
    join dim_asset_service as das on fpr.asset_id = das.asset_id''')

```
<b>LabOwnerSNOW.py</b> - Populates the `lab owners` table in ServiceNow with data from a static excel file containing IP ranges and lab owners. <br>
<b>SNOW.py</b> - Automatically creates and populates an incident table using the report generated from Rapid7 Nexpose. <br>
<b>lab_owner_snow.py</b> -  Filter through the `lab owners` table and match the first octect of the IP address associated with a critical vulnerability from the Nexpose scan report to find the name of the lab owner.<br>
<b>MatchOwner.py</b> - imports the `get_lab_owner_by_ip` method from the <b>lab_owner_snow.py</b> and match the whole IP address with one of the IP addresses from the `lab owners` table.   

## Deployment

Run it on the requested server and implement [ ... ]

## Stretch Goals 

-Implementation of Carbon Black, McAfee, and other security tools during the scanning and remediation phase, so that the information can be consolidated and pulled to populate the ticket <br> 
-Automate monthly security reports on dashboards in ServiceNow 

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments



<br>
