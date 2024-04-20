def debug_mode(oa, command):
    selected_mails = oa.select_mails(command)
    for mail in selected_mails:
        print(mail.subject, " / ", mail.datetime_received)
    # oa.mark_read(selected_mails)
    # oa.delete(selected_mails)

    # oa.bulk_delete(command)
    oa.folders()