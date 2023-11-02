import ast

from django.shortcuts import render
from .models import LotteryUserMapping
# Create your views here.
from datetime import datetime
# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AddPaymentDetailsInBulk  # Import your form
from .models import LotteryPayment  # Import your model


def process_payment(request):
    queryset = request.session.get('queryset')
    # print('query_set===> ', queryset)
    if request.method == 'POST':
        form = AddPaymentDetailsInBulk(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            orderMonth = form.cleaned_data['orderMonth']
            paymentMode = form.cleaned_data['paymentMode']
            records_to_create = []

            # Perform your custom action with the additional data on selected objects.
            for id in queryset:
                obj = LotteryUserMapping.objects.get(id=id)
                records_to_create.append(LotteryPayment(lotteryUserMappingId=obj, amount=amount, orderMonth=orderMonth, paymentMode=paymentMode))

            LotteryPayment.objects.bulk_create(records_to_create)
            messages.success(request, "Bulk Record added successfully.")
            original_url = request.GET.get('original_url')

            if original_url:
                return redirect(original_url)
            else:
                # Handle cases where there is no original URL (provide a default URL to go back to)
                return redirect(f'admin/kitty/lotteryusermapping/')
            # return redirect('admin:kitty/lotteryusermapping/')  # Redirect to the admin list view
        else:
            messages.error(request, 'An error occurred!')
    else:
        form = AddPaymentDetailsInBulk()

    return render(request, 'kitty/add_payment_detail.html', {'form': form})

from django.views import View
from django.db import connection
from .models import Lottery
from django.core.paginator import Paginator, EmptyPage


class PivotTable(View):

    def pagination_html_code(self, total_pages, active_page_number, next_page_url, previous_page_url):
        pagination_html_code = ""

        if active_page_number is not None and int(active_page_number) > 1:
            pagination_html_code = f"""
                            <li class="page-item">
                                <a class="page-link" href="{previous_page_url}">Previous</a>
                            </li>"""
        for page in range(1, total_pages+1):
            if active_page_number is not None and page == active_page_number:
                pagination_html_code += f"""
                    <li class="page-item"><a class="page-link" href="?page={page}">{page}</a></li>
                    <li class="page-item active" aria-current="{page}"></li>"""
            else:
                pagination_html_code += f"""
                    <li class="page-item"><a class="page-link" href="?page={page}">{page}</a></li>
                    <li class="page-item"></li>"""

        if active_page_number is not None and int(active_page_number) != total_pages:
            pagination_html_code += f"""
                <li class="page-item">
                    <a class="page-link" href="{next_page_url}">Next</a>
                </li>
            """

        return pagination_html_code

#     def generate_sql_quary(self, start_date, end_date, lottery_id):
#         months = ['Januaray', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
#                   'November', 'December']
#         sql_queries = []
#         # top sql query
#         sql_query1 = "SELECT lotteryNumber, userName,"
#         sql_query2 = "SELECT "
#         # Convert the start_date and end_date strings to datetime objects
#         start_date = datetime.strptime(start_date, "%Y-%m-%d")
#         end_date = datetime.strptime(end_date, "%Y-%m-%d")
#
#         # Loop through the months between start_date and end_date
#         current_date = start_date
#         while current_date <= end_date:
#             # Extract the year and month and add to the result list
#             year = current_date.year
#             month = current_date.month
#             # middle sql query
#
#             sql_query_case = f"SUM(CASE WHEN month(orderMonth) = {month:02d} and year(orderMonth)={year} THEN amount ELSE 0 END) AS {months[(month) - 1]}{year},\n"
#             sql_query1 += sql_query_case
#             sql_query2 += sql_query_case
#             # sql_query_case = f'SUM(CASE WHEN strftime("%m",orderMonth) = {month:02d} and strftime("%Y",orderMonth)={year} THEN amount ELSE 0 END) AS {months[(month) - 1]}{year},\n'
#             # sql_query += sql_query_case
#             # Move to the next month
#             if current_date.month == 12:
#                 current_date = current_date.replace(year=current_date.year + 1, month=1)
#             else:
#                 current_date = current_date.replace(month=current_date.month + 1)
#                 print('===> ', current_date)
#         # bottom sql query
#         sql_query1 += f"""(SELECT (CASE WHEN sum(amount) > 0 THEN sum(amount) ELSE 0 END) FROM kitty_lotterypayment WHERE kitty_lotterypayment.lotteryUserMappingId_id = kitty_lotteryusermapping.id) AS total_amount
# FROM kitty_lotteryusermapping
# LEFT JOIN kitty_lotterypayment ON  kitty_lotteryusermapping.id = kitty_lotterypayment.lotteryUserMappingId_id
# where kitty_lotteryusermapping.lotteryId_id={lottery_id}
# GROUP BY kitty_lotteryusermapping.id;
# """
#         sql_query2 += f"""
#         SUM(amount) FROM kitty_lotterypayment
# LEFT JOIN kitty_lotteryusermapping ON  kitty_lotteryusermapping.id = kitty_lotterypayment.lotteryUserMappingId_id
# where kitty_lotteryusermapping.lotteryId_id={lottery_id}
# GROUP BY kitty_lotteryusermapping.lotteryId_id;
# """
#         sql_queries.append(sql_query1)
#         sql_queries.append(sql_query2)
#         # add total amount rows
#         return sql_queries

    def generate_sql_quary(self, start_date, end_date, lottery_id):
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
        sql_queries = []
        # top sql query
        sql_query1 = "SELECT lotteryNumber, userName,"
        sql_query2 = "SELECT "
        # Convert the start_date and end_date strings to datetime objects
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        # Loop through the months between start_date and end_date
        current_date = start_date
        while current_date <= end_date:
            # Extract the year and month and add to the result list
            year = current_date.year
            month = current_date.month
            # middle sql query

            sql_query_case = f"SUM(CASE WHEN month(orderMonth) = {month:02d} and year(orderMonth)={year} THEN amount ELSE 0 END) AS {months[(month) - 1]}{year},\n"
            sql_query1 += sql_query_case
            sql_query2 += sql_query_case

            # Move to the next month
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1, day=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1, day=1)
            print('===> ', current_date)

        # bottom sql query
        sql_query1 += f"""discount,gift, (SELECT (CASE WHEN sum(amount) != 0 THEN sum(amount) ELSE 0 END) FROM kitty_lotterypayment WHERE kitty_lotterypayment.lotteryUserMappingId_id = kitty_lotteryusermapping.id) AS total_amount
    FROM kitty_lotteryusermapping
    LEFT JOIN kitty_lotterypayment ON  kitty_lotteryusermapping.id = kitty_lotterypayment.lotteryUserMappingId_id
    where kitty_lotteryusermapping.lotteryId_id={lottery_id}
    GROUP BY kitty_lotteryusermapping.id;
    """
        sql_query2 += f"""(SELECT SUM(discount) from kitty_lotteryusermapping where kitty_lotteryusermapping.lotteryId_id={lottery_id}) as Discount,
        (SELECT sum(gift) from kitty_lotteryusermapping where kitty_lotteryusermapping.lotteryId_id={lottery_id}) as Gift,
        SUM(amount) FROM kitty_lotterypayment
    LEFT JOIN kitty_lotteryusermapping ON  kitty_lotteryusermapping.id = kitty_lotterypayment.lotteryUserMappingId_id
    where kitty_lotteryusermapping.lotteryId_id={lottery_id}
    GROUP BY kitty_lotteryusermapping.lotteryId_id;
    """
        sql_queries.append(sql_query1)
        sql_queries.append(sql_query2)
        # add total amount rows
        return sql_queries

    def get(self, request, lottery_id, **kwargs):
        obj = Lottery.objects.get(id=lottery_id)

        raw_sql_query = self.generate_sql_quary(str(obj.startDate.date()), str(obj.endDate.date()), lottery_id)
        print(raw_sql_query[1])

        with connection.cursor() as cursor:
            cursor.execute(raw_sql_query[0])

            # Fetch the results if needed
            results = cursor.fetchall()
            # Get column names from the cursor description
            columns = [col[0] for col in cursor.description]

            cursor.execute(raw_sql_query[1])
            monthly_total_amount = cursor.fetchall()

        paginator = Paginator(results, 100)  # 10 rows per page
        page_number = request.GET.get('page', 1)

        try:
            page = paginator.get_page(page_number)
        except EmptyPage:
            page = paginator.get_page(1)  # Default to the first page if page number is out of range

        # Get the URLs for next and previous pages
        next_page_url = f'?page={page.next_page_number()}' if page.has_next() else None
        prev_page_url = f'?page={page.previous_page_number()}' if page.has_previous() else None
        total_pages = page.paginator.num_pages
        context = {
            'columns': columns,
            'rows': page,
            # 'pagination': self.pagination_html_code(total_pages, page_number, next_page_url, prev_page_url),
            'lottery_name': obj.lotteryName,
            'monthly_total_amount': monthly_total_amount,
        }
        if total_pages > 1:
            context['pagination'] = self.pagination_html_code(total_pages, page_number, next_page_url, prev_page_url)
        return render(request, 'kitty/lottery_pivot_table.html', context)


class showDetailsOfPendingAmount(View):
    def get_queryset(self):
        sql_query = """
            select lotteryId_id,
            kitty_lottery.lotteryName, 
            kitty_lottery.amount,
            date(kitty_lottery.startDate) as startDate, 
            userName, lotteryNumber, 
            discount, 
            sum(kitty_lotterypayment.amount)+discount as total_paid,
            IF(DAY(CURRENT_DATE) < DAY(kitty_lottery.startDate),
                   (PERIOD_DIFF(DATE_FORMAT(CURRENT_DATE, '%Y%m'), DATE_FORMAT(date(kitty_lottery.startDate), '%Y%m')))*kitty_lottery.amount - (sum(kitty_lotterypayment.amount)+discount),
                   (PERIOD_DIFF(DATE_FORMAT(CURRENT_DATE, '%Y%m'), DATE_FORMAT(date(kitty_lottery.startDate), '%Y%m'))+1)*kitty_lottery.amount -(sum(kitty_lotterypayment.amount)+discount)
               ) AS pending_months_amount
            from kitty_lotteryusermapping
            left join kitty_lotterypayment on kitty_lotterypayment.lotteryUserMappingId_id = kitty_lotteryusermapping.id 
            join kitty_lottery on kitty_lottery.id = kitty_lotteryusermapping.lotteryId_id
            group by kitty_lotteryusermapping.id
            HAVING pending_months_amount > 0 and total_paid >0;
        """
        with connection.cursor() as cursor:
            cursor.execute(sql_query)

            # Fetch the results if needed
            results = cursor.fetchall()
            # Get column names from the cursor description
            columns = [col[0] for col in cursor.description]

        return results, columns

    def get(self, request):

        queryset, columns = self.get_queryset()

        print("queryset ==> ", queryset)
        print("columns name ==> ", columns)

        context = {
            'columns': columns,
            'rows': queryset
        }

        return render(request, 'kitty/pending_amount_record.html', context)

