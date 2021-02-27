region = "eu-central-1"
default_tags = {
  Name : "udacity-DE-NanoDegree",
  project : "project3-dwh"
}

vpc_cidr_block              = "10.0.0.0/16"
number_of_redshift_subnets  = 2
redshift_subnet_group_name  = "udacity-project3"
redshift_role_name          = "udacity-project3-redshift-role"
redshift_cluster_identifier = "udacity-project3-cluster"

redshift_database_name   = "dev"
redshift_node_type       = "dc2.large"
redshift_cluster_port    = 5439