
# Integration of AWS Services with Financial Analytics System (FAS)

This document provides a detailed walkthrough of each AWS service integrated into the **Financial Analytics System (FAS)** project, showcasing the sequence of integrations, goals, challenges, and outcomes.

---

## 1. Amazon S3: Secure Data Storage

**Purpose**: Initially set up Amazon S3 as a storage solution for backing up forex data and any intermediate files.

**Setup Summary**:
- **Bucket Creation**: Created a private S3 bucket to store data securely.
- **IAM Policy and Permissions**: Configured IAM policies to restrict access, allowing only the necessary services and users to read/write from the bucket.

**Challenges**: None initially; S3 served as a straightforward storage solution.

## 2. Amazon RDS: Database Setup for PostgreSQL

**Purpose**: Use Amazon RDS to host a PostgreSQL database for storing forex data, historical prices, and analytics results.

**Setup Summary**:
- **RDS Instance Creation**: Set up a PostgreSQL instance within a private subnet for added security.
- **Security Configuration**:
  - **VPC Configuration**: Placed RDS within a VPC, ensuring it was accessible only from specified IPs.
  - **Security Group Rules**: Restricted inbound access to only the OpenVPN EC2 instance.

**Challenges**: Needed a secure, VPN-only connection to the RDS instance to prevent unauthorized access.

## 3. EC2 Instance with OpenVPN for Secure RDS Access

**Purpose**: Secure the connection to RDS by setting up an EC2 instance to run OpenVPN, ensuring only authorized clients access the database.

**Setup Summary**:
- **Instance Configuration**:
  - Launched an EC2 instance with Amazon Linux for the VPN server.
  - Installed and configured OpenVPN with Easy-RSA to handle client-server authentication.
  - Enabled IP forwarding and applied `iptables` rules for secure traffic handling.

- **Client Connection**:
  - Used `Tunnelblick` as the client application on macOS to connect to the VPN, allowing secure access from the client machine to the OpenVPN server on EC2 and then to the RDS instance.

- **Firewall Configuration**:
  - Configured security groups and Network ACLs to allow OpenVPN traffic and restrict database access to only VPN clients.
  
**Challenges**:
  - Ensuring secure certificate management with Easy-RSA.
  - Managing IP forwarding and firewall rules to allow controlled RDS access.

## 4. AWS Lambda: Scheduled Data Fetching from OANDA API

**Purpose**: Automate weekly data fetching of EURUSD forex data from the OANDA API, to be stored in PostgreSQL for analysis.

**Setup Summary**:
- **Function Creation**:
  - Created a Lambda function to fetch and process forex data from the OANDA API.
  - Set up IAM permissions for Lambda to access AWS Secrets Manager and RDS.

- **Secrets Manager Integration**:
  - Stored OANDA API credentials and RDS connection details in Secrets Manager for secure access.
  
**Challenges**:
  - Encountered issues integrating `psycopg2` with Lambda due to the absence of necessary PostgreSQL libraries, which required packaging psycopg2 with Lambda layers.

**Outcome**: Due to these challenges, automated fetching was not fully implemented; the project was later shifted to a manual refresh system.

## Transition to Free Cloud Services

With AWS free-tier limits exhausted, the project was transitioned to **Neon**, a cost-effective PostgreSQL alternative, while retaining the core project objectives. Automated data fetching through Lambda was replaced with a refresh button in the Dash app, allowing user-controlled data updates.

---

### Summary of AWS Integration

The project’s AWS integration journey illustrates a strong understanding of cloud services, security best practices, and the challenges inherent in working with production-level cloud infrastructure.
