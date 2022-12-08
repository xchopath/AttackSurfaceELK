## Setup

### Elasticsearch Server
```
curl -X PUT http://server:9200/assetdomain
curl -X PUT http://server:9200/assethttp
curl -X PUT http://server:9200/httpscan
curl -X PUT http://server:9200/assetnet
curl -X PUT http://server:9200/netscan
```

### Agent

1. Install ProjectDiscovery's Tools.
```
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest
```

2. Clone this repository
```
git clone https://github.com/xchopath/AttackSurfaceELK
cd AttackSurfaceELK/
```

3. Install Python3 requirements
```
pip3 install -r requirements.txt
```

4. Copy and Adjust `.env`
```
cp .env.example .env
vim .env
```

## Run

### Run Script
```
bash runner.sh
```

### Daily Crontab
```
0 0 * * * bash /path-to/AttackSurfaceELK/runner.sh
```
