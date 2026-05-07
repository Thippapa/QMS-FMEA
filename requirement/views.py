from django.shortcuts import render
from django.db import connection
from django.conf import settings

from .models import RequirementDocument


def is_demo_mode():
    return not settings.DEBUG


def requirement_list(request):
    if is_demo_mode():
        documents = [
            {
                "DocumentName": "Process FMEA - Assembly Line",
                "DocumentType": "FMEA",
                "RevisionNumber": 3,
                "Status": "Active",
            },
            {
                "DocumentName": "Control Plan - Welding Process",
                "DocumentType": "Control Plan",
                "RevisionNumber": 2,
                "Status": "Active",
            },
        ]

        return render(request, 'requirement/requirement_list.html', {
            'documents': documents
        })

    documents = RequirementDocument.objects.all()

    return render(request, 'requirement/requirement_list.html', {
        'documents': documents
    })


def model_dashboard(request):
    if is_demo_mode():
        documents = [
            {
                "DocumentName": "Assembly FMEA",
                "Components": "Bracket A",
                "Description1": "Step 10 - Fitment Check",
                "Description2": "Risk review for assembly process",
                "ResponsibleName": "Engineer A",
                "PrepareBy": "Quality Team",
                "RevisionNumber": 3,
                "OriginatedDate": "2026-01-10",
                "RevisionDate": "2026-04-20",
                "DocModifiedDate": "2026-05-01",
            },
            {
                "DocumentName": "Welding FMEA",
                "Components": "Frame B",
                "Description1": "Step 20 - Weld Inspection",
                "Description2": "Control welding defect risk",
                "ResponsibleName": "Engineer B",
                "PrepareBy": "Process Team",
                "RevisionNumber": 2,
                "OriginatedDate": "2026-02-05",
                "RevisionDate": "2026-04-25",
                "DocModifiedDate": "2026-05-02",
            },
        ]
    else:
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
    if is_demo_mode():
        approvals = [
            {
                "DocumentID": 1,
                "DocumentName": "Assembly FMEA",
                "StatusName": "Pending for Approve",
                "ApprovalRequestDate": "2026-05-01",
                "ResponsibleuserID": 101,
                "ResponsibleName": "Engineer A",
                "ApprovalGroupUserID": 201,
                "LoggedInName": "Approver A",
                "ApprovalActionTakenDate": None,
                "RevisionNumber": 3,
                "ApproverNotes": "Waiting for review",
            },
            {
                "DocumentID": 2,
                "DocumentName": "Welding FMEA",
                "StatusName": "Approval Approved",
                "ApprovalRequestDate": "2026-04-25",
                "ResponsibleuserID": 102,
                "ResponsibleName": "Engineer B",
                "ApprovalGroupUserID": 202,
                "LoggedInName": "Approver B",
                "ApprovalActionTakenDate": "2026-04-28",
                "RevisionNumber": 2,
                "ApproverNotes": "Approved",
            },
        ]
    else:
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
    if is_demo_mode():
        cp_records = [
            {
                "DocumentID": 1,
                "ProcessNumber": "10",
                "ProcessName": "Assembly",
                "Machine": "ASM-01",
                "Number": "PC-001",
                "Product": "Bracket dimension",
                "Process": "",
                "SPEC": "10.0 ± 0.2 mm",
                "Measurement": "Vernier Caliper",
                "SampleSize": "5 pcs",
                "FREQ": "Every 2 hours",
                "ControlMethod": "Inspection record",
                "ReactionPlan": "Stop line and inform engineer",
                "Description1": "Assembly FMEA",
            },
            {
                "DocumentID": 2,
                "ProcessNumber": "20",
                "ProcessName": "Welding",
                "Machine": "WLD-02",
                "Number": "PC-002",
                "Product": "",
                "Process": "Weld strength",
                "SPEC": "No crack / full penetration",
                "Measurement": "Visual + destructive test",
                "SampleSize": "3 pcs",
                "FREQ": "Per lot",
                "ControlMethod": "Welding parameter check",
                "ReactionPlan": "Quarantine lot",
                "Description1": "Welding FMEA",
            },
        ]
    else:
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