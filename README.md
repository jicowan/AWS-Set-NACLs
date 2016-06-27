# AWS-Set-NACLs
Creates a NACL that blocks port 23 inbound on all subnets in a VPC.  Rules are evaluated in sequential order (highest to lowest).  If there are no matching rules, the default deny all rule will apply.
