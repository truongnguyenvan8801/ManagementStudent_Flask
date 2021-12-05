from flask_admin import BaseView
from my_app.admin import *


class MyStudentIndexView(AdminIndexView):
	@expose('/')
	def index(self):
		if not current_user.is_authenticated or current_user.is_student() == False:
			flash('Please log in first...', category='danger')
			# next_url = request.url
			# login_url = '%s?next=%s' % (url_for('login_page'), next_url)
			return redirect(url_for('login_page'))
		users = User.query.filter_by(id=current_user.user_id).first()
		self._template_args["info"] = users
		return super(MyStudentIndexView,self).index()
	
class MyBaseStudentView(MyBaseView):
	def is_accessible(self):
		return current_user.is_student()

	def inaccessible_callback(self, name, **kwargs):
		flash('Yêu cầu truy cập không khả dụng!! Hãy đăng nhập', category='danger')
		return redirect(url_for('login_page'))

class PersonalInfoView_Student(MyBaseStudentView):
	list_template = 'student/info.html'
	@expose('/')
	def info_view(self):
		return super(PersonalInfoView_Student,self).list_view()

	edit_template = 'student/edit_info.html'

	@expose('/edit', methods=['GET','POST'])
	def edit_view(self):
		update_info_form = UpdateInfoForm()
		if request.method == "POST":
			more_info = MoreInfo.query.filter_by(user_id=current_user.user_id).first()
			if more_info is not None:
				more_info.email = update_info_form.u_email.data
				more_info.phone = update_info_form.u_phone.data
				more_info.current_residence = update_info_form.u_residence.data
				more_info.note = update_info_form.note.data
			else: 
				more_info = MoreInfo(user_id=current_user.user_id,email=update_info_form.u_email.data,phone=update_info_form.u_phone.data,current_residence=update_info_form.u_residence.data,note=update_info_form.note.data,modified_at=datetime.now())
				db.session.add(more_info)
			student_to_update = Student.query.filter_by(user_id=current_user.user_id).first()
			family_info = FamilyInfo.query.filter_by(student_id=student_to_update.id).first()
			if family_info is not None:
				family_info.full_name = update_info_form.contact_name.data
				family_info.phone = update_info_form.contact_phone.data
				family_info.current_residence = update_info_form.contact_residence.data
			family_info = FamilyInfo(student_id=student_to_update.id, full_name=update_info_form.contact_name.data, phone=update_info_form.contact_phone.data, current_residence=update_info_form.contact_residence.data, modified_at=datetime.now())
			db.session.add(family_info)

			db.session.commit()
			return redirect(url_for('student_info.info_view'))
		more_info = MoreInfo.query.filter_by(user_id=current_user.user_id)
		return self.render('student/edit_info.html', update_info_form=update_info_form, more_info=more_info)

	def render(self, template, **kwargs):
		student = Student.query.filter_by(user_id=current_user.user_id).first()
		family_info = FamilyInfo.query.filter_by(student_id=student.id).first()
		kwargs['student'] = student
		kwargs['family_info'] = family_info
		return super(PersonalInfoView_Student, self).render(template, **kwargs)

class ConfirmView_Student(BaseView):
	@expose('/')
	def index(self):
		image_fields = ResumeImageFields.query.filter_by(role_id=current_user.role_id).all()
		resume_student = Resume.query.filter_by(user_id=current_user.user.id).first()
		if resume_student:
			resume_images = [{str(image.field_id): image.image_path} for image in ResumeImageStorage.query.filter_by(resume_id=resume_student.id).all()]
			# resume_images = ResumeImageStorage.query.filter_by(resume_id=resume_student.id).all()
			self._template_args["resume_images"] = resume_images
			flash('Hồ sơ của bạn đang chờ được duyệt !!!', category='danger')
		self._template_args["image_fields"] = image_fields
		return self.render('student/confirm.html')

	@expose('/submit', methods=['GET','POST'])
	def submit(self):
		image_fields = ResumeImageFields.query.filter_by(role_id=current_user.role_id).all()
		if request.method == 'POST':
			resume = Resume(user_id=current_user.user.id)
			db.session.add(resume)
			db.session.commit()
			for field in image_fields:
				info = cloudinary.uploader.upload(request.files[str(field.id)])
				save = ResumeImageStorage(resume_id=resume.id, field_id=field.id, image_path=info['secure_url'], image_public_id=info['public_id'])
				db.session.add(save)
				db.session.commit()
			flash('Nộp hồ sơ thành công !!! Hồ sơ của bạn đang ở hàng chờ để duyệt.', category='success')
			return redirect(url_for('_confirmStudent.index'))
			# list_images = []
			# # print(request.files)
			# for field in image_fields:
			# 	print(request.files[field.id])
			# 	list_images.append(request.files[field.id])
			# return Response(
			# 	json.dumps({"msg": request.files}),
			# 	status=200,
			# 	mimetype='application/json'
			# )
			# return redirect(url_for('_student.index'))


# class SubmitConfirmView_Student(BaseView):
# 	@expose('/', methods=["POST"])
# 	def index(self):
# 		if request.method == 'POST':

# 		users = Account.query.filter_by(user_id=current_user.user_id).update(dict(active=1))
# 		db.session.commit()
# 		flash(f'Đăng nhập thành công !!!', category='success')
# 		return redirect(url_for('_student.index'))

class ChangePasswordView_Student(ChangePasswordView):
	@expose('/', methods=['GET','POST'])
	def index(self):
		return super(ChangePasswordView_Student, self).index()

student = Admin(app, name='Student', index_view=MyStudentIndexView(url='/student', endpoint='_student'), base_template='master.html', template_mode='bootstrap4', url='/student', endpoint='_student')
student.add_view(PersonalInfoView_Student(MoreInfo,db.session, name='Thông tin cá nhân', url='/student/info', endpoint='student_info', menu_icon_type="ti", menu_icon_value="ti-pencil"))
student.add_view(ConfirmView_Student(name="confirm", url='/student/confirm', endpoint='_confirmStudent'))

#student.add_view(SubmitConfirmView_Student(name="submitConfirm", url='/student/confirm/submit', endpoint='_submitConfirmStudent'))
student.add_view(ChangePasswordView_Student(name="Đổi mật khẩu", url="/student/change-password", endpoint='_changePasswordStudent'))
