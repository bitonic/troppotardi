import logging

from datetime import datetime
from copy import deepcopy

from pylons import request, response, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators.rest import restrict, dispatch_on
from pylons.decorators import validate

from troppotardi.lib.base import BaseController, render
from troppotardi.model import Image, User
from troppotardi.model.forms import AddUser, EditUser, EditImage
from troppotardi.lib.helpers import flash
from troppotardi.lib.utils import generate_password, send_email
from troppotardi.lib import authorize
from troppotardi.lib.mapping import day_to_str

class AdminController(BaseController):

    def index(self):
        redirect(url(controller='admin', action='pending'))

    @authorize('review_images')
    @dispatch_on(POST='_dopending')
    def pending(self):
        c.images = Image.pending_by_time(self.db,
                                         descending=True)

        return render('/admin/pending.mako')

    @authorize('review_images')
    @restrict('POST')
    def _dopending(self):
        # These are all the images ticked with accept
        to_accept = request.POST.getall('accept')
        
        # Accept all of them
        for id in to_accept:
            image = Image.load(self.db, id)
            image.state = 'accepted'
            image.store(self.db)
        
        # These are the ones to delete
        to_delete = request.POST.getall('delete')
        
        # Delete them
        for id in to_delete:
            Image.load(self.db, id).delete(self.db)
            
        redirect(url(controller='admin', action='pending'))

    @authorize('review_images')
    @dispatch_on(POST='_dopending')
    def accepted(self):
        # Handles the pagination in a really simple way
        startkey = request.GET.get('startkey')
        endkey = request.GET.get('endkey')

        if startkey:
            c.images = list(Image.by_day(self.db, descending=True, startkey=startkey, limit=16))
        elif endkey:
            c.images = list(Image.by_day(self.db, descending=False, startkey=endkey, limit=16))
            c.images.reverse()
        else:
            c.images = list(Image.by_day(self.db, descending=True, limit=16))

        c.nextkey = c.prevkey = None
        if c.images:
            # If it's 16 elements long, save the key to get the next images
            # and remove the last element (which serves just to see the next key)
            if len(c.images) == 16:
                c.nextkey = day_to_str(c.images[-1].day)
                c.images = c.images[:-1]
                
            # If the image is not the first one, then save the key to get the
            # previous images
            if c.images[0].id != list(Image.by_day(self.db, descending=True, limit=1))[0].id:
                c.prevkey = day_to_str(c.images[0].day)

        return render('/admin/accepted.mako')

    @authorize('review_images')
    @restrict('POST')
    def _doaccepted(self):
        to_delete = request.POST.getall('delete')
        
        # Delete them
        for id in to_delete:
            Image.load(self.db, id).delete(self.db)
            
        redirect(url(controller='admin', action='accepted'))

    @authorize('review_images')
    @dispatch_on(POST='_dodeleted')
    def deleted(self):
        c.images = Image.deleted_by_time(self.db, descending=True)

        return render('/admin/deleted.mako')

    @authorize('delete_images')
    @restrict('POST')
    def _dodeleted(self):
        to_delete = request.POST.getall('delete')

        for id in to_delete:
            Image.load(self.db, id).delete_permanently(self.db)

        redirect(url(controller='admin', action='deleted'))

    @authorize('review_images')
    @dispatch_on(POST='_doedit')
    def edit(self, id):
        c.image = Image.load(self.db, id)

        return render('/admin/edit.mako')

    @authorize('review_images')
    @restrict('POST')
    @validate(schema=EditImage(), form='edit')
    def _doedit(self, id):
        image = Image.load(self.db, id)
        
        image.author = request.params.getone('author')
        image.author_email = request.params.getone('author_email')
        image.author_url = request.params.getone('author_url')
        image.text = request.params.getone('text')

        # "change_day" is a hidden field that indicates that the date
        # is exposed in the form. we don't change the day if we are
        # setting the image to pending, since this creates problems
        # when detecting if the image has changed date
        if ('change_day' in self.form_result) and request.params.getone('state') == 'accepted':
            image.day = datetime(year=int(self.form_result.get('year')),
                                 month=int(self.form_result.get('month')),
                                 day=int(self.form_result.get('day')))
        
        image.state = self.form_result.get('state')

        image.store(self.db)

        flash('Image successfully edited')
        redirect(url(controller='admin', action='edit', id=id))
    
    @authorize('manage_users')
    @dispatch_on(POST='_doadduser')
    def adduser(self):
        c.roles = User.roles

        return render('/admin/adduser.mako')
    
    @authorize('manage_users')
    @restrict('POST')
    @validate(schema=AddUser(), form='adduser')
    def _doadduser(self):
        user = User()
        
        user.username = c.username = request.params.getone('username')
        user.email = request.params.getone('email')
        user.role = request.params.getone('role')
        
        c.password = generate_password()
        user.password = c.password

        # Sends the email
        send_email(render('/emails/registration.mako'),
                   'Welcome to troppotardi',
                   [user.email])
        
        user.store(self.db)
        
        flash('User added successfully, an email has been sent with the password.')
        redirect(url(controller='admin', action='adduser'))

    @authorize('manage_users')
    def users(self):
        c.users = User.by_username(self.db, descending=True)
        
        return render('/admin/users.mako')

    @authorize('manage_users')
    @dispatch_on(POST='_doedit_user')
    def edit_user(self, id):
        c.user = User.load(self.db, id)
        c.roles = User.roles

        return render('/admin/edit_user.mako')
    
    @authorize('manage_users')
    @validate(schema=EditUser(), form='edit_user')
    def _doedit_user(self, id):
        user = User.load(self.db, id)
        
        user.username = self.form_result.get('username')
        user.email = self.form_result.get('email')
        user.role = self.form_result.get('role')
        
        if self.form_result.get('password'):
            user.password = self.form_result.get('password')

        user.store(self.db)
        
        flash('User successfully edited.')
        redirect(url(controller='admin', action='edit_user', id=id))

    @authorize('manage_users')
    def delete_user(self, id):
        User.load(self.db, id).delete(self.db)

        flash('User deleted.')

        redirect(url(controller='admin', action='users'))
        
    @authorize('list_authors')
    def authors(self):
        c.images = Image.by_day(self.db)

        return render('/admin/authors.mako')
