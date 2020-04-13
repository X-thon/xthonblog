import os

from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, send_from_directory
from flask_login import login_required, current_user
from flask_ckeditor import upload_success, upload_fail

from xthonblog.extensions import db, cache
from xthonblog.forms import SettingForm, PasswordField, CategoryForm, LinkForm
from xthonblog.models import Post, Category, Comment, Link
from xthonblog.utils import redirect_back

admin_bp = Blueprint("admin", __name__)

@admin_bp.route('/settings', methods=['GET', 'POST'])
@cache.cached(timeout=60)
@login_required
def settings():
    form = SettingForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.blog_title = form.blog_title.data
        current_user.blog_sub_title = form.blog_sub_title.data
        #current_user.about = form.about.data
        current_user.introduction = form.introduction.data
        current_user.location = form.location.data
        db.session.commit()
        flash('Setting updated.', 'success')
        return redirect(url_for('blog.index'))
    form.name.data = current_user.name
    form.blog_title.data = current_user.blog_title
    form.blog_sub_title.data = current_user.blog_sub_title
    #form.about.data = current_user.about
    form.introduction.data = current_user.introduction
    form.location.data = current_user.location
    return render_template('admin/settings.html', form=form)



#管理所有文章的页面
@admin_bp.route('/post/manage')
@login_required
def manage_post():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['BLUELOG_MANAGE_POST_PER_PAGE'])
    posts = pagination.items
    return render_template('admin/manage_post.html', page=page, pagination=pagination, posts=posts)



#删除文章
@admin_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.', 'success')
    return redirect_back()