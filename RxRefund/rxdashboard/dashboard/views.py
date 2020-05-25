from django.shortcuts import render
from dashboard.forms import dateforms

from django.db import connection

from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

from django.http import JsonResponse
import locale
locale.setlocale(locale.LC_ALL, '')

def date_form(request):
    f1 = dateforms()
    if request.method == 'POST':
        f1 = dateforms(request.POST)

    return render(request, 'dateinput.html', {'f1': f1})

def index(request):
    return render(request, 'index.html')


class date_inf:
    date_input=""

def dashboard(request):
    year_input = request.POST['year_input']
    month_input = request.POST['month_input']
    calender = {'1' : '31', '2' :'28', '3' :'31', '4':'30', '5':'31', '6':'30', '7':'31', '8':'31','9':'30',\
                '10':'31','11':'30','12':'31'}

    first_date =year_input+"-"+month_input+"-"+"1"
    last_date = year_input + "-" + month_input + "-" + calender[month_input]

    date_inf.date_input=month_input+"-"+year_input


    with connection.cursor() as cursor:


        cursor.execute("SELECT gdc,description,sum(cast(qty_dispensed  AS DECIMAL(8,2))) as volume,\
                                                        cast((sum(cast(margin AS DECIMAL(8,2))))/(sum(cast(profit AS DECIMAL(8,2)))) as decimal(8,2)) as revenue,\
                                                      sum(cast(acquisition_costs AS DECIMAL(8,2))) as total_acquisition_cost,\
                                                     sum(cast(profit AS DECIMAL(8,2))) as profit,sum(cast(margin  AS DECIMAL(8,2))) as margin,\
                                                     cast(sum(cast(acquisition_costs  AS DECIMAL(8,2)))/ sum(cast(qty_dispensed  AS DECIMAL(8,2))) as decimal(8,2)) AS total_acq_unit_cost,\
                                                      drug_manufacturer\
                                                      FROM dashboard_transaction_table \
                                                     WHERE date_filled between '" + first_date + "' and '" + last_date + "' and generic='"'generic'"'\
                                                     AND status = '"'rx'"' GROUP BY gdc,description,drug_manufacturer order by margin ASC LIMIT 25")

        table = dictfetchall(cursor)
        for i in table:
            i["gdc"]=round(float(i["gdc"]))
            i["total_acquisition_cost"]=float(i["total_acq_unit_cost"])*float(i["volume"])
            i["total_acquisition_cost"] = round(float(i["total_acquisition_cost"]),2)
            i["revenue"]=float(i["profit"])/float(i["margin"])
            i["revenue"]=round(float(i["revenue"]),2)


    return render(request, 'MainPage.html', {'table': table})


def calculation_page(request):
    return render(request, 'calculations.html')

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

class SignUpView(CreateView):
    template_name = 'MainPage.html'
    form_class = UserCreationForm

def validate_username(request):


    gcn = request.GET.get('GCN', None)
    description = request.GET.get('Description', None)
    volume = request.GET.get('Volume', None)
    #volume=floorf(volume * 100 + 0.5) / 100;
    totalrevenue = request.GET.get('Total Revenue', None)
    profit = request.GET.get('Profit', None)
    margin = request.GET.get('Margin', None)
    unitcost = request.GET.get('Unit Cost', None)
    alternativeunitcost = request.GET.get('Alternative Unit Cost', None)
    savingswithalternativecost = request.GET.get('Savings With Alternative Cost', None)
    drugmanufacturer = request.GET.get('Drug Manufacturer', None)
    unitcost = unitcost.split('$')
    totalcost = request.GET.get('Total Cost ', float(volume) * float(unitcost[1]))
    #totalcost=totalcost.split('$')
    totalrevenue=totalrevenue.split('$')
    profit = profit.split('$')
    margin = margin.split('%')
    if alternativeunitcost == "":
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO dashboard_dashboard_page_table(gcn,description,volume,total_revenue,total_cost,profit,margin,unit_cost,alternative_unit_cost,savinsg_with_alternative_unit_cost,drug_manufacturer,date_filled)"
                "values('" + str(gcn) + "','" + str(description) + "','" + str(volume) + "'," + totalrevenue[1] + ",'"+str(totalcost)+"'," + profit[1] + "," + margin[0] + "," + unitcost[1] + ",null ,null,'" + str(drugmanufacturer) + "','" + date_inf.date_input + "')")

    with connection.cursor() as cursor:
         cursor.execute("INSERT INTO dashboard_dashboard_page_table(gcn,description,volume,total_revenue,total_cost,profit,margin,unit_cost,alternative_unit_cost,savinsg_with_alternative_unit_cost,drug_manufacturer,date_filled)"
                       "values('"+str(gcn)+"','"+str(description)+"','"+str(volume)+"',"+totalrevenue[1]+",'"+str(totalcost)+"',"+profit[1]+","+margin[0]+","+unitcost[1]+","+alternativeunitcost+","+savingswithalternativecost+",'"+str(drugmanufacturer)+"','" + date_inf.date_input + "')")


    data = {

    }

    return JsonResponse(data)


def summary_page(request):
    # summary calculation for January 2019

    # total rx number in 2019 Jan
    with connection.cursor() as c:
        c.execute('select COUNT (*) from dashboard_transaction_table '
                  'where date_filled between '" '2019-01-01'  "' and '"'2019-01-31'"'')
        total_rx_jan_19 = c.fetchone()

    # total sales for revenue in 2019 Jan
    with connection.cursor() as c:
        c.execute('select sum(cast(total_sales AS DECIMAL(8,2))) from dashboard_transaction_table '
                  'where date_filled between '" '2019-01-01'"' and '"'2019-01-31'"'')
        total_revenue_jan_2019 = c.fetchone()

    # total acquisiton cost in 2019 Jan
    with connection.cursor() as c:
        c.execute('select sum(cast(acquisition_costs AS DECIMAL(8,2))) from dashboard_transaction_table '
                  'where date_filled between '" '2019-01-01 ' "' and '"'2019-01-31'"'')
        total_acq_cost_jan_2019 = c.fetchone()

    # margin in 2019 Jan
    with connection.cursor() as c:
        c.execute('SELECT SUM(cast(margin AS DECIMAL(8,2))) FROM dashboard_transaction_table '
                  'where date_filled between '" '2019-01-01 ' "' and '"'2019-01-31'"'')
      #  margin_jan_2019 = c.fetchone()

    gross_profit_jan_2019 = round(float(total_revenue_jan_2019[0]) - float(total_acq_cost_jan_2019[0]), 2)

    # Avg Revenue calculation for 2019 jan
    avg_revenue_jan_2019 = round(float(total_revenue_jan_2019[0]) / float(total_rx_jan_19[0]), 2)

    # Avg COG calculation for 2019 jan
    avg_cog_jan_2019 = round(float(total_acq_cost_jan_2019[0]) / float(total_rx_jan_19[0]), 2)

    # Avg Gross profit calculation for 2019 jan
    avg_gross_profit_jan_2019 = round(float(gross_profit_jan_2019) / float(total_rx_jan_19[0]), 2)

    #margin_jan_2019 = float(gross_profit_jan_2019) /float(total_revenue_jan_2019[0]) #yuvarlanmamis hali

    margin_jan_2019 = round(float(gross_profit_jan_2019) /float(total_revenue_jan_2019[0]), 2) # yuvarlanmis hali

    january = {"total": total_rx_jan_19[0], "revenue": '{:,}'.format(total_revenue_jan_2019[0]), "acq": '{:,}'.format(total_acq_cost_jan_2019[0]), \
               "gross_profit": '{:,}'.format(gross_profit_jan_2019), "avg_revenue": '{:,}'.format(avg_revenue_jan_2019), "avg_cog": '{:,}'.format(avg_cog_jan_2019), \
               "avg_profit": '{:,}'.format(avg_gross_profit_jan_2019), "margin": "{0:.0%}".format(margin_jan_2019) }

    # summary calculation for December 2018
    with connection.cursor() as c:
        c.execute('select COUNT (*) from dashboard_transaction_table '
                  'where date_filled between '" '2018-12-01'  "' and '"'2018-12-31'"'')
        total_rx_dec_18 = c.fetchone()

        # total sales for revenue in December 2018
    with connection.cursor() as c:
        c.execute('select sum(cast(total_sales AS DECIMAL(8,2))) from dashboard_transaction_table '
                  'where date_filled between '" ' 2018-12-01'"' and '"'2018-12-31'"'')
        total_revenue_dec_18 = c.fetchone()

        # total acquisiton cost in December 2018
    with connection.cursor() as c:
        c.execute('select sum(cast(acquisition_costs AS DECIMAL(8,2))) from dashboard_transaction_table '
                  'where date_filled between '" '2018-12-01 ' "' and '"'2018-12-31'"'')
        total_acq_cost_dec_18 = c.fetchone()

        # margin in December 2018 burasi iptal ama silme sonra duzeltiriz commentleri
    with connection.cursor() as c:
        c.execute('SELECT SUM(cast(margin AS DECIMAL(8,2))) FROM dashboard_transaction_table '
                  'where date_filled between '" '2018-12-01 ' "' and '"'2018-12-31'"'')
      #  margin_dec_18 = c.fetchone()

        # Gross profit calculation for December 2018
    gross_profit_dec_18 = round(float(total_revenue_dec_18[0]) - float(total_acq_cost_dec_18[0]), 2)

    # Avg Revenue calculation for December 2018
    avg_revenue_dec_18 = round(float(total_revenue_dec_18[0]) / float(total_rx_dec_18[0]), 2)

    # Avg COG calculation for December 2018
    avg_cog_dec_18 = round(float(total_acq_cost_dec_18[0]) / float(total_rx_dec_18[0]), 2)

    # Avg Gross profit calculation for December 2018
    avg_gross_profit_dec_18 = round(float(gross_profit_dec_18) / float(total_rx_dec_18[0]), 2)

    #margin_dec_18 = float(gross_profit_dec_18) / float(total_revenue_dec_18[0]) # yuvarlanmamis hali
    #print(gross_profit_dec_18)
    #print(total_revenue_dec_18)
    #"{0:.0%}".format(1. / 3)
    margin_dec_18 = round( float(gross_profit_dec_18) / float(total_revenue_dec_18[0]), 2) # yuvarlanmis hali

    december = {"total": total_rx_dec_18[0], "revenue": '{:,}'.format(total_revenue_dec_18[0]), "acq": '{:,}'.format(total_acq_cost_dec_18[0]), \
                "gross_profit": '{:,}'.format(gross_profit_dec_18), "avg_revenue": '{:,}'.format(avg_revenue_dec_18), "avg_cog": '{:,}'.format(avg_cog_dec_18), \
                "avg_profit": '{:,}'.format(avg_gross_profit_dec_18), "margin":  "{0:.0%}".format(margin_dec_18)}

    # summary calculation for November 2018
    with connection.cursor() as c:
        c.execute('select COUNT (*) from dashboard_transaction_table '
                  'where date_filled between '" '2018-11-01'  "' and '"'2018-11-30'"'')
        total_rx_nov_18 = c.fetchone()

        # total sales for revenue in November 2018
    with connection.cursor() as c:
        c.execute('select sum(cast(total_sales AS DECIMAL(8,2))) from dashboard_transaction_table '
                  'where date_filled between '" ' 2018-11-01'"' and '"'2018-11-30'"'')
        total_revenue_nov_18 = c.fetchone()

        # total acquisiton cost in November 2018
    with connection.cursor() as c:
        c.execute('select sum(cast(acquisition_costs AS DECIMAL(8,2))) from dashboard_transaction_table '
                  'where date_filled between '" '2018-11-01' "' and '"'2018-11-30'"'')
        total_acq_cost_nov_18 = c.fetchone()

        # margin in November 2018
    # with connection.cursor() as c:
    #     c.execute('SELECT SUM(cast(margin AS DECIMAL(8,2))) FROM dashboard_transaction_table '
    #               'where date_filled between '" '2018-11-01 ' "' and '"'2018-11-30'"'')
      #  margin_nov_18 = c.fetchone()

        # Gross profit calculation for November 2018
    gross_profit_nov_18 = round(float(total_revenue_nov_18[0]) - float(total_acq_cost_nov_18[0]), 2)

    # Avg Revenue calculation for November 2018
    avg_revenue_nov_18 = round(float(total_revenue_nov_18[0]) / float(total_rx_nov_18[0]), 2)

    # Avg COG calculation for November 2018
    avg_cog_nov_18 = round(float(total_acq_cost_nov_18[0]) / float(total_rx_nov_18[0]), 2)

    # Avg Gross profit calculation for November 2018
    avg_gross_profit_nov_18 = round(float(gross_profit_nov_18) / float(total_rx_nov_18[0]), 2)

    margin_nov_18 = float(gross_profit_nov_18) / float(total_revenue_dec_18[0]) #yuvarlanmamis hali

    #yuvarlanmis margin icin margin_nov_18 = round( float(gross_profit_nov_18) / float(total_revenue_dec_18[0]), 2)



    november = {"total": total_rx_nov_18[0], "revenue": '{:,}'.format(total_revenue_nov_18[0]), "acq": '{:,}'.format(total_acq_cost_nov_18[0]), \
                "gross_profit":'{:,}'.format( gross_profit_nov_18), "avg_revenue": '{:,}'.format(avg_revenue_nov_18), "avg_cog": '{:,}'.format(avg_cog_nov_18), \
                "avg_profit": '{:,}'.format(avg_gross_profit_nov_18), "margin": "{0:.0%}".format(margin_nov_18)}

    return render(request, 'summary.html', context={'january': january, 'december': december, 'november': november})
