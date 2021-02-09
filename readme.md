# yearn exporter

collects on-chain numeric data about yearn vault and exposes it in prometheus format.

point prometheus at this exporter persist the data and make it queryable.

set up grafana for custom dashboards and alerts.


## usage

```
brownie run yearn exporter_v1 --network mainnet
brownie run yearn exporter_v2 --network mainnet
brownie run yearn exporter_experimental --network mainnet

```

## Docker setup

```
export GF_SECURITY_ADMIN_USER=<YOUR_ADMIN_USER> # only after changing it, default is admin
export GF_SECURITY_ADMIN_PASSWORD=<YOUR_ADMIN_PASSWORD> # only after changing it, default is admin
export WEB3_INFURA_PROJECT_ID=<YOUR_PROJECT_ID>
./run.sh
```

After successful startup you can go directly to grafana at `http://localhost:3000` and login with `admin:admin`.

## supported vaults

the goal of the project is to collect advanced metrics about vaults and strategies.
