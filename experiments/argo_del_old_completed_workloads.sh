# usage: argo_del_old_completed_workloads.sh <age>
argo delete -n dl-argo-events --older $1
