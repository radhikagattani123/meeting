import frappe
from frappe import _
from frappe.utils import nowdate,add_days
import datetime

@frappe.whitelist()
def send_invitation_emails(meeting):
	meeting = frappe.get_doc("Meeting" , meeting)
	meeting.check_permission("email")

	if meeting.status == "Planned":
		# print "inside sent invitation ==\n\n",meeting.__dict__
		print "************8\n\n\n",type(meeting.invitation_message),meeting.attendees
		a = [d.attendee for d in meeting.attendees]
		print a,"\n\n\nnattendeeeeeeeeeeesssssssssssssssss"

		frappe.sendmail(
			recipients = a, 
			sender =  frappe.session.user,
			subject = meeting.title,
			message = meeting.invitation_message,
			reference_doctype = meeting.doctype, 
			reference_name = meeting.name,
			as_bulk = True
			)

		meeting.status = "Invitation Sent"
		meeting.save()

		frappe.msgprint(_("Invitation Sent!"))

	# else
	# 	frappe.msgprint(_("Meeting status must be Planned"))	

@frappe.whitelist()
def get_meetings(from_date,to_date):
	print "\n\n\n hello ======"
	# if not frappe.check_permission("Meeting","read")
	# 	raise frappe.PermissionError
	
	# return frappe.db.sql(""" select
	# 	timestamp(`date`,from_time) as start,
	# 	timestamp(`date`,to_time) as end,
	# 	name,
	# 	title,
	# 	status,
	# 	0 as all_day
	# 	from `tabMeeting`
	# 	where `date` between %(start)s and %(end)s""" ,{
	# 	"from_date" : start,
	# 	"to_date" : end
	# 	},as_dict = true)

@frappe.whitelist()
def make_orientation_meeting(doc,method):
	""" Create an orientation meeting when a new user is added"""
	print "\n\n\n doc ----- method  ===========",doc.name
	if frappe.db.exists("User", doc.name): 
		user_doc = frappe.get_doc("User",doc.name)
		meet_doc = frappe.new_doc("Meeting")
		meet_doc.title = "Orientation for {0}".format(doc.first_name)
		meet_doc.date = add_days(nowdate(),1)
		meet_doc.status = "Planned"
		attendees = meet_doc.append("attendees",{})
		attendees.attendee = user_doc.name
		# meet_doc.attendees = [{"attendee" : doc.name}]
		meet_doc.save()

		# meeting = frappe.get_doc({
		# 	"doc_type" : "Meeting",
		# 	"title" : "Orientation for {0}".format(doc.first_name),
		# 	"date" : add_days(nowdate(),1),
		# 	"from_time" : "09:00",
		# 	"to_time" : "09:30",
		# 	"status" : "Planned",
		# 	"attendees" : [{
		# 		"attendee" : user_doc.name,
		# 	}]
		# }) 

	# the system manager might not have permissions to create a meeting
	# meeting.flags.ignore_permissions = True
	# meeting.insert()
	frappe.msgprint(_("Orientation meeting created"))

