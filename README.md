<img align = "left" src="https://i.imgur.com/g89b9Na.png">
<br><br><br><br>
A solution to improve security operations through the automation and harmonic orchestration of tools that deal with threat intelligence management, security event management, and SecOps processes. The SOAR project aims to create a centralized system to more easily access, manage, and remediate security incidents in lab endpoints, effectively decreasing incident response times while increasing the efficiency of the security/devOps process.



## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

-Python 2.7 <br>
-<a href="https://github.com/rbw0/pysnow">Pysnow Library</a><br>
-<a href="https://github.com/rapid7/vm-console-client-python/blob/master/rapid7vmconsole/rest.py">Rapid7 Nexpose Library</a><br>
-ForeScout CounterAct<br>
-Rapid7 Nexpose<br>
-ServiceNow 

### Installing

Download Python 2.7 and install the libraries listed in the prerequisites. Make sure to have admin access and credentials to ForeScout, Rapid7 Nexpose, and ServiceNow to be able to successfully test policies, workflows, and the code. 


## The Code
<b>nexpose.py</b> - REST API that generates csv reports from the most recent Rapid7 Nexpose scans into a readable format for ServiceNow. Using the <a href="https://help.rapid7.com/nexpose/en-us/warehouse/warehouse-schema.html">Nexpose ER Diagram</a>, the SQL query below can be easily customized to add or remove additional columns of information in the final generated report.<br> 
```
report_id = create_report_sql(report_client, 'vulnReport', '''
    select da.asset_id, da.mac_address, da.ip_address, das.port, dv.vulnerability_id, 
        dv.title, dv.description, dv.severity, dv.cvss_score, dv.exploits, dv.nexpose_id
    from fact_asset_vulnerability_finding as fpr 
    join dim_vulnerability as dv on fpr.vulnerability_id = dv.vulnerability_id 
    join dim_asset as da on fpr.asset_id = da.asset_id 
    join dim_asset_service as das on fpr.asset_id = das.asset_id''')

```
##### Generated reports are found in the Reports tab in Rapid7 Nexpose:<br>

<img src="https://i.imgur.com/TMBPKey.png">
<b>LabOwnerSNOW.py</b> - Populates the `u_lab_owners_list` table in ServiceNow with data from a static excel file containing IP ranges and lab owners. <br>
<br><b>SNOW.py</b> - Automatically creates and populates an incident table using the report generated from Rapid7 Nexpose. <br><br>
<b>lab_owner_snow.py</b> -  Filter through the `lab owners` table and match the first octect of the IP address associated with a critical vulnerability from the Nexpose scan report to find the name of the lab owner.<br><br>
<b>MatchOwner.py</b> - imports the `get_lab_owner_by_ip` method from the <b>lab_owner_snow.py</b> and match the whole IP address with one of the IP addresses from the `lab owners` table.   

## Deployment

##### Windows
Deploy with as a scheduled task

##### Linux
Deploy as a cronjob

## Common Errors
-When running `nexpose.py` make sure that the name of the to-be generated report does not already exist in the Nexpose 'Reports' tab. Another option is to make sure the report file is deleted after it is generated.<br>

##### Example: 
``` 
report_id = create_report_sql(report_client,'vulnReport', '''
```

## Success Criteria

-ForeScout detects all connected endpoint devices on the network<br>
-All new devices are added to ServiceNow's `cmdb_ci_computer` table<br>
-Labs with a CVSS score of 7-10 are automatically quarantined through ForeScout<br>
-Labs detected with a vulnerability must have an incident ticket created. Incidents with a high CVSS score are prioritized and sent immediately to the IR team. <br>
-All lab owners will receive an email when their lab device has been quarantined or a vulnerability has been detected <br>
-All lab devices will have a point of contact, so that if an issue were to arise, contact can quickly be made.

## Stretch Goals 

-Implementation of Carbon Black, McAfee, and other security tools during the scanning and remediation phase, so that the information can be consolidated and pulled to populate the ticket <br> 

-Automate monthly security reports on dashboards in ServiceNow

-Have the lab owner information, which is currently a static excel, dynamically updated and pulled into ServiceNow 

## Authors
 Alondra Macias, Avanthika Ramesh, Dabin Cheon, Yousef Bajes, Jordan Bates

### Acknowledgments
Thank you <a href="https://github.com/rbw0/pysnow">Pysnow Library</a> and <a href="https://github.com/rapid7/vm-console-client-python/blob/master/rapid7vmconsole/rest.py">Rapid7 Nexpose Library</a>. <br>

Another thank you to Scott Theriault, Kumar, Awasti Abhishek, John Weaver, Nathan Michelena, Shlomo Bielak, Matt Cole, and Noah Heil for their help and advice throughout this whole process. 



<br>
