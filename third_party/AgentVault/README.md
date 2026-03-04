# AgentVault: Secure Agent Credential Management

A secure credential management system for AI agents, enabling encrypted storage, controlled sharing, and comprehensive audit logging.

## Overview

AgentVault provides a secure way for AI agents to:
- Store credentials in encrypted vaults
- Share credentials between agents with granular permissions
- Maintain comprehensive audit logs of all credential operations
- Integrate with OpenClaw and Claude-based workflows

## Installation

```bash
pip install agentvault
```

Or install from source:

```bash
git clone https://github.com/nKOxxx/agentvault.git
cd agentvault
pip install -e .
```

## Quick Start

### Creating a Secure Vault

```python
from agentvault import Vault, VaultConfig

# Create a new vault with encryption
config = VaultConfig(
    encryption_key="your-secure-key-here",
    vault_name="my-agent-vault"
)
vault = Vault(config)

# Initialize the vault
vault.initialize()
```

### Adding Credentials

```python
from agentvault import Credential

# Create a credential
credential = Credential(
    name="api-key-openai",
    value="sk-...",
    metadata={
        "service": "openai",
        "environment": "production",
        "rotation_date": "2024-12-31"
    }
)

# Store in vault
vault.store_credential(credential)
```

### Retrieving Credentials

```python
# Retrieve a credential
credential = vault.get_credential("api-key-openai")
print(f"API Key: {credential.value}")
print(f"Metadata: {credential.metadata}")
```

### Sharing Credentials Between Agents

```python
from agentvault import SharingPolicy

# Define sharing policy
policy = SharingPolicy(
    allowed_agents=["agent-123", "agent-456"],
    permissions=["read"],
    expiration="2024-12-31T23:59:59Z"
)

# Share credential
vault.share_credential(
    credential_name="api-key-openai",
    policy=policy
)
```

### Receiving Shared Credentials

```python
from agentvault import SharedVault

# Connect to a shared vault
shared = SharedVault(
    vault_url="https://vault.example.com/shared/abc123",
    agent_id="agent-123"
)

# List available credentials
available = shared.list_credentials()

# Access shared credential
credential = shared.get_credential("shared-api-key")
```

### Audit Logging

```python
from agentvault import AuditLogger

# Configure audit logging
logger = AuditLogger(
    vault=vault,
    log_destination="file",  # or "stdout", "remote"
    log_path="/var/log/agentvault/audit.log"
)

# All operations are automatically logged
# View recent activity
recent = logger.get_recent_logs(limit=10)
for entry in recent:
    print(f"{entry.timestamp}: {entry.action} - {entry.credential_name}")
```

## Security Best Practices

### 1. Encryption Key Management

```python
from agentvault import KeyManager

# Use a hardware security module or key management service
key_manager = KeyManager(
    backend="aws-kms",  # or "azure-keyvault", "gcp-kms", "hashicorp-vault"
    key_id="alias/agentvault-master"
)

config = VaultConfig(
    key_manager=key_manager,
    encryption_algorithm="AES-256-GCM"
)
```

### 2. Credential Rotation

```python
from agentvault import RotationPolicy

# Set up automatic rotation
policy = RotationPolicy(
    credential_name="api-key-openai",
    rotation_interval_days=90,
    notification_before_days=7
)

vault.enable_rotation(policy)
```

### 3. Access Control

```python
from agentvault import AccessControl

# Define fine-grained access control
acl = AccessControl()
acl.add_rule(
    agent_id="agent-123",
    allowed_operations=["read", "list"],
    allowed_credentials=["api-key-openai", "db-password"]
)

vault.set_access_control(acl)
```

### 4. Secure Environment Variables

```python
import os
from agentvault import VaultConfig

# Never hardcode encryption keys
config = VaultConfig(
    encryption_key=os.environ["AGENTVAULT_MASTER_KEY"],
    vault_name=os.environ.get("AGENTVAULT_NAME", "default")
)
```

## OpenClaw Integration

AgentVault integrates seamlessly with OpenClaw for secure credential management in agent workflows:

```python
from agentvault import OpenClawIntegration
from openclaw import Agent

# Initialize OpenClaw integration
vault_integration = OpenClawIntegration(
    vault=vault,
    auto_inject=True  # Automatically inject credentials into agent context
)

# Create agent with secure credential access
agent = Agent(
    name="secure-agent",
    credentials=vault_integration.get_credentials_for_agent("secure-agent")
)

# Credentials are automatically available to the agent
# but never exposed in logs or conversation history
```

### Environment Variable Integration

```python
# In your OpenClaw agent configuration
import os
from agentvault import Vault

# Load vault from environment
vault = Vault.from_environment()

# Credentials are securely injected
api_key = vault.get_credential("openai-api-key").value
os.environ["OPENAI_API_KEY"] = api_key
```

## Complete Example

See [agentvault_example.py](./agentvault_example.py) for a complete working example demonstrating all features.

## Advanced Features

### Multi-Vault Management

```python
from agentvault import VaultManager

# Manage multiple vaults
manager = VaultManager()
manager.create_vault("production")
manager.create_vault("staging")
manager.create_vault("development")

# Switch between vaults
prod_vault = manager.get_vault("production")
```

### Backup and Recovery

```python
# Create encrypted backup
vault.backup(
    destination="s3://my-bucket/agentvault-backups/",
    encrypt_with="gpg-key-id"
)

# Restore from backup
vault.restore(
    source="s3://my-bucket/agentvault-backups/backup-2024-01-01.enc"
)
```

## Troubleshooting

### Common Issues

**Issue**: `EncryptionKeyError: Invalid key format`
- **Solution**: Ensure your encryption key is at least 32 characters for AES-256

**Issue**: `CredentialNotFoundError`
- **Solution**: Check the credential name and verify it exists in the vault

**Issue**: `AccessDeniedError`
- **Solution**: Verify your agent has the necessary permissions in the access control list

## Related Resources

- [AgentVault GitHub Repository](https://github.com/nKOxxx/agentvault)
- [OpenClaw Documentation](https://openclaw.io/docs)
- [Claude API Documentation](https://docs.anthropic.com)

## License

MIT License - See AgentVault repository for details.
