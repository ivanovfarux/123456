import django_tables2 as tables
# from  models import Product
from ticket.models import Problem, Compleks, Company

class ProblemHTMxMultiColumnTable(tables.Table):
    class Meta:
        model = Problem
        show_header = False
        template_name = "tables/bootstrap_col_filter.html"