variable "project_name" { type=string default="medlake" }
variable "environment" { type=string default="dev" }
variable "location" { type=string default="centralindia" }
variable "tags" { type=map(string) default={workload="healthcare-data-platform",managed="terraform"} }
