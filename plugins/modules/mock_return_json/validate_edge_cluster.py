import json
import yaml
def validate_edge_cluster_payload():
    return {
        "id": "bf0a448f-cb77-419f-be4d-652cc2826b57",
        "description": "Validating NSX Edge cluster creation spec",
        "executionStatus": "IN_PROGRESS",
        "resultStatus": "UNKNOWN",
        "validationChecks": [
            {
                "description": "Validate Edge Node Management IP to FQDN Resolution",
                "resultStatus": "UNKNOWN"
            },
            {
                "description": "Validate Distinct Uplink Interfaces per Edge Node",
                "resultStatus": "UNKNOWN"
            },
            {
                "description": "Validate Tier-1 Gateway Name Does Not Exist",
                "resultStatus": "UNKNOWN"
            },
            {
                "description": "Validate the specified NSX enabled VDS uplinks are prepared for Edge overlay",
                "resultStatus": "UNKNOWN"
            },
            {
                "description": "Check vSphere cluster has all hosts with a vCPU count and RAM size to accommodate the selected Edge form factor",
                "resultStatus": "UNKNOWN"
            },
            {
                "description": "Validate IP Address Assigned to Same Subnet",
                "resultStatus": "UNKNOWN"
            },
            {
                "description": "Validate Edge Node Overlay (TEP) IPs are Unique",
                "resultStatus": "UNKNOWN"
            },
            {
                "description": "Validate Edge Cluster Name Does Not Exist",
                "resultStatus": "UNKNOWN"
            },
            {
                "description": "Validate Management Network is Reachable",
                "resultStatus": "UNKNOWN"
            },
            {
                "description": "Validate Edge Node Passwords Against NSX Password Policy",
                "resultStatus": "UNKNOWN"
            },
            {
                "description": "Check for unique IPs for Edge management IP, Edge TEP IPs, Tier-0 uplink interface IPs & BGP Peer IPs across Edge Nodes.",
                "resultStatus": "UNKNOWN"
            },
            {
                "description": "Validate that TEP IPs, gateway, and management IP, gateway are in the same subnet",
                "resultStatus": "UNKNOWN"
            },
            {
                "description": "Validate Edge Cluster Name Does Not Exist in NSX Manager",
                "resultStatus": "UNKNOWN"
            },
            {
                "description": "Validate that the specified IP addresses in the input spec do not conflict with the Tier-0 transit subnets",
                "resultStatus": "UNKNOWN"
            },
            {
                "description": "Check that the custom Edge cluster profile does not conflict with an existing profile",
                "resultStatus": "UNKNOWN"
            },
            {
                "description": "Validate Edge Node FQDNs are Unique",
                "resultStatus": "UNKNOWN"
            },
            {
                "description": "Validate L2 Non-Uniform and L3 Cluster",
                "resultStatus": "UNKNOWN"
            },
            {
                "description": "Validate all vCenter clusters are either all stretched or none are stretched",
                "resultStatus": "UNKNOWN"
            },
            {
                "description": "Validate IP Address Conflicts",
                "resultStatus": "UNKNOWN"
            },
            {
                "description": "Validate Tier-0 Gateway Name Does Not Exist",
                "resultStatus": "UNKNOWN"
            },
            {
                "description": "Validate vSphere Cluster Belongs to the Workload Domain",
                "resultStatus": "UNKNOWN"
            },
            {
                "description": "Validate Uplink VLANs",
                "resultStatus": "UNKNOWN"
            },
            {
                "description": "Validate Capacity for Hosting vSphere Cluster",
                "resultStatus": "UNKNOWN"
            },
            {
                "description": "Validate Routing Between Host Overlay (TEP) and Edge Overlay (TEP)",
                "resultStatus": "UNKNOWN"
            },
            {
                "description": "Validate each Edge node's VLAN is consistent per vSphere cluster",
                "resultStatus": "UNKNOWN"
            },
            {
                "description": "Check for unique IPs for Edge management IP, Edge TEP IPs, Tier-0 uplink interface IPs",
                "resultStatus": "UNKNOWN"
            }
        ]
    }