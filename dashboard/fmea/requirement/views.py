from django.shortcuts import render
from django.db import connection

from .models import RequirementDocument


def requirement_list(request):
    documents = RequirementDocument.objects.all()

    return render(request, 'requirement/requirement_list.html', {
        'documents': documents
    })


def model_dashboard(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                DocumentName,
                Components,
                Description1,
                Description2,
                ResponsibleName,
                PrepareBy,
                RevisionNumber,
                OriginatedDate,
                RevisionDate,
                DocModifiedDate
            FROM ModelDashboard
        """)

        columns = [col[0] for col in cursor.description]

        documents = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    total_document_names = len({
        doc['DocumentName']
        for doc in documents
        if doc.get('DocumentName')
    })

    total_step_adopt_model_names = len({
        doc['Description1']
        for doc in documents
        if doc.get('Description1')
    })

    document_names = sorted({
        doc['DocumentName']
        for doc in documents
        if doc.get('DocumentName')
    })

    step_adopt_names = sorted({
        doc['Description1']
        for doc in documents
        if doc.get('Description1')
    })

    return render(request, 'requirement/model_dashboard.html', {
        'documents': documents,
        'total_document_names': total_document_names,
        'total_step_adopt_model_names': total_step_adopt_model_names,
        'document_names': document_names,
        'step_adopt_names': step_adopt_names,
    })

def approve_dashboard(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                DocumentID,
                DocumentName,
                StatusName,
                ApprovalRequestDate,
                ResponsibleuserID,
                ResponsibleName,
                ApprovalGroupUserID,
                LoggedInName,
                ApprovalActionTakenDate,
                RevisionNumber,
                ApproverNotes
            FROM ApproveDashboard
        """)

        columns = [col[0] for col in cursor.description]
        approvals = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    total_rows = len(approvals)

    unique_documents = len({
        item['DocumentName']
        for item in approvals
        if item.get('DocumentName')
    })

    pending_count = sum(
        1 for item in approvals
        if item.get('StatusName') == 'Pending for Approve'
    )

    approved_count = sum(
        1 for item in approvals
        if item.get('StatusName') == 'Approval Approved'
    )

    rejected_count = sum(
        1 for item in approvals
        if item.get('StatusName') == 'Approval Rejected'
    )

    document_names = sorted({
        item['DocumentName']
        for item in approvals
        if item.get('DocumentName')
    })

    return render(request, 'requirement/approve_dashboard.html', {
        'approvals': approvals,
        'total_rows': total_rows,
        'unique_documents': unique_documents,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'document_names': document_names,
    })

def cp_form(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                DocumentID,
                ProcessNumber,
                ProcessName,
                Machine,
                Number,
                Product,
                Process,
                SPEC,
                Measurement,
                SampleSize,
                FREQ,
                ControlMethod,
                ReactionPlan,
                Description1
            FROM CPform
        """)

        columns = [col[0] for col in cursor.description]

        cp_records = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    document_names = sorted({
        item['Description1']
        for item in cp_records
        if item.get('Description1')
    })

    return render(request, 'requirement/cp_form.html', {
        'cp_records': cp_records,
        'document_names': document_names,
        'total_records': len(cp_records),
    })

def home(request):
    return render(request, 'requirement/home.html')