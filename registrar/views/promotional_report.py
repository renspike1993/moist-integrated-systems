# views.py
import csv
from django.contrib import messages
from django.shortcuts import render, redirect
from ..models import PromotionalReport
from ..forms import PromotionalReportImportForm
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count,Q
from django.core.paginator import Paginator




@login_required
@permission_required('registrar.view_promotionalreport', login_url='accounts:login')
def promotional_report_summary(request):
    """
    Shows PromotionalReport grouped by year and semester, with count of rows for each.
    """
    # Group by year and semester
    summary = (
        PromotionalReport.objects
        .values('semester','year')
        .annotate(total_students=Count('last_name'))
        .order_by('year')
    )

    context = {
        'summary': summary
    }
    return render(request, 'promotional-report/promotional_report_summary.html', context)


@login_required
@permission_required('registrar.view_promotionalreport', login_url='accounts:login')
def promotional_detail(request, year, semester):
    query = request.GET.get('q', '')  # Get search query from GET parameter

    records_list = PromotionalReport.objects.filter(year=year, semester=semester)

    if query:
        records_list = records_list.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )

    records_list = records_list.order_by('last_name', 'first_name')

    # Pagination: 100 records per page
    paginator = Paginator(records_list, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'year': year,
        'semester': semester,
        'page_obj': page_obj,
        'query': query,  # pass current search term to template
    }
    return render(request, 'promotional-report/promotional_detail.html', context)


@login_required
@permission_required('registrar.add_promotionalreport', login_url='accounts:login')
def import_promotional_report(request):
    if request.method == 'POST':
        form = PromotionalReportImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']

            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File is not CSV type')
                return redirect('registrar:import_promotional_report')

            # Decode CSV file
            file_data = csv_file.read().decode("utf-8")
            lines = file_data.splitlines()
            reader = csv.DictReader(lines)

            for row in reader:
                try:
                    PromotionalReport.objects.create(
                        year=row.get('year'),
                        semester=row.get('semester'),
                        first_name=row.get('first_name'),
                        last_name=row.get('last_name'),
                        sub_code=row.get('sub_code'),
                        sub_desc=row.get('sub_desc'),
                        grade=row.get('grade'),
                        units=int(row.get('units') or 0),  # <--- safely convert
                        source_file=row.get('source_file'),
                    )
                except ValueError:
                    # skip invalid rows
                    continue

            messages.success(request, f"Promotional Report imported successfully from {csv_file.name}")
            return redirect('registrar:import_promotional_report')
    else:
        form = PromotionalReportImportForm()

    return render(request, 'promotional-report/import_promotional_report.html', {'form': form})
