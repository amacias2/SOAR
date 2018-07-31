<img align = "left" src="https://i.imgur.com/g89b9Na.png">
<br><br><br><br>
A solution to improve security operations through the automation and harmonic orchestration of tools that deal with threat intelligence management, security event management, and SecOps processes. The SOAR project aims to create a centralized system to more easily access, manage, and remediate security incidents in lab endpoints, effectively decreasing incident response times while increasing the efficiency of the security/devOps process.



## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

-Python 2.7 <br>
-<a href="https://github.com/rbw0/pysnow">Pysnow Library</a><br>
-<a href="https://github.com/rbw0/pysnow">Rapid7 Nexpose Library</a><br>
-<a href="https://github.com/rbw0/pysnow">SharePoint Library</a><br>
-Forescout CounterAct<br>
-Rapid7 Nexpose<br>
-Service Now 

```
Give examples
```

### Installing

Download Python 2.7 and install the libraries listed in the prerequisites. Make sure to have admin access and credentials to ForeScout, Rapid7 Nexpose, and ServiceNow to be able to successfully test policies, workflows, and the code. 


## Running the tests
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
<b>SNOW.py</b> - Automatically creates and populates an incident table using the 

### Break down into end to end tests

Explain what these tests test and why



```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc


<br>
