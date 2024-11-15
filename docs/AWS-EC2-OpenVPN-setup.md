
# EC2 Instance Setup for OpenVPN (High-Level)

This document provides an overview of the steps to set up an EC2 instance as an OpenVPN server for securely accessing the RDS PostgreSQL database in the **Financial Analytics System (FAS)** project.

---

## 1. Launch an EC2 Instance

1. **Instance Type**: Choose an Amazon Linux or Ubuntu instance.
2. **Security Group**: 
   - Allow inbound traffic on port `1194` (UDP) for OpenVPN.
   - Allow inbound traffic for SSH (port `22`) to manage the instance.
3. **Elastic IP**: Associate an Elastic IP to the instance for consistent access.

## 2. Install and Configure OpenVPN

1. **Install OpenVPN and Easy-RSA**: Use the following commands after connecting to the instance:
   ```bash
   sudo yum install -y openvpn easy-rsa
   ```

2. **Set Up Easy-RSA for Certificates**:
   - Initialise the CA, generate server keys, and create client keys using Easy-RSA.

3. **Configure OpenVPN Server**:
   - Edit the `server.conf` file to define VPN settings such as network address, pushed routes, and security settings (e.g., `tls-auth`, `cipher`, `keepalive`).

## 3. Enable IP Forwarding and Configure Firewall

1. **IP Forwarding**: Enable IP forwarding in the system.
   ```bash
   sudo sysctl -w net.ipv4.ip_forward=1
   ```
2. **Firewall Rules**: Use `iptables` to allow traffic between the VPN and private subnets hosting the RDS instance.

## 4. Client Configuration

1. **Generate Client Configuration**: Create a `client.ovpn` configuration file with necessary server details, including the `ca`, `cert`, and `key` files.
2. **Distribute Configuration**: Share `client.ovpn` with authorised users for secure access to the VPN.

## 5. Test the VPN Connection

1. Verify connection from the client to the RDS instance via the VPN.
2. Troubleshoot connectivity issues, if any, by reviewing OpenVPN and system logs.

---