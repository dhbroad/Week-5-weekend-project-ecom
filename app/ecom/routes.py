from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required


ecom = Blueprint('ecom', __name__, template_folder='ecom_templates')

from .forms import CreatePostForm, UpdatePostForm
from app.models import db, Post, Cart



@ecom.route('/posts')
def posts():
#     title1 = 'A Rock'
#     img_url1 = 'https://m.media-amazon.com/images/I/61m9jG+jj-L._AC_SX466_.jpg'
#     caption1 = "It's a Rock."
#     price1 = 20.00

#     ep1 = (title1, img_url1, caption1, price1)

#     title2 = "Fancy Chair"
#     img_url2 = "https://cdn.shopify.com/s/files/1/0326/0841/products/nice-black-occasional-chairs-lifestyle_1200x.jpg?v=1604086309"
#     caption2 = "When you sit in this chair, you'll feel fancy"
#     price2= 200.00

#     ep2=(title2, img_url2, caption2, price2)
    
#     existing_posts = [ep1,ep2]

    posts = Post.query.all()[::-1]

    return render_template('posts.html', posts = posts)


@ecom.route('/create-post', methods=["GET", "POST"])
@login_required
def createPost():
    form = CreatePostForm()
    if request.method == "POST":
        if form.validate():
            title = form.title.data
            img_url = form.img_url.data
            caption = form.caption.data
            price = form.price.data

            post = Post(title, img_url, caption, price, current_user.id)

            db.session.add(post)
            db.session.commit()   

            return redirect(url_for('home'))         

    return render_template('createpost.html', form = form)

@ecom.route('/posts/<int:post_id>')
def individualPost(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return redirect(url_for('ecom.posts'))
    return render_template('individual_post.html', post = post)

@ecom.route('/posts/update/<int:post_id>', methods=["GET","POST"]) # you GET the website and you UPDATE the information
@login_required
def updatePost(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return redirect(url_for('ecom.posts'))
    if post.user_id != current_user.id:
        return redirect(url_for('ecom.posts'))
    form = UpdatePostForm()
    if request.method == "POST":
        if form.validate():
            title = form.title.data
            img_url = form.img_url.data
            caption = form.caption.data
            price = form.price.data

            # update the original post
            post.title = title
            post.image = img_url
            post.caption = caption
            post.price = price

            db.session.commit()   

            return redirect(url_for('home'))         
    return render_template('updatepost.html', form=form, post = post)


@ecom.route('/posts/delete/<int:post_id>', methods=["POST"]) # not a GET request because you are really just POSTing to delete
@login_required
def deletePost(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return redirect(url_for('ecom.posts'))
    if post.user_id != current_user.id:
        return redirect(url_for('ecom.posts'))

    db.session.delete(post)
    db.session.commit()
               
    return redirect(url_for('ecom.posts')) # redirecting to the homepage


@ecom.route('/add-to-cart', methods=["GET", "POST"])
@login_required
def addToCart():
    form = CreatePostForm()
    if request.method == "POST":
        title = form.title.data
        img_url = form.img_url.data
        caption = form.caption.data
        price = form.price.data

        cart_items = Cart(title, img_url, caption, price)

        db.session.add(cart_items)
        db.session.commit()   

        return redirect(url_for('home'))         

    return render_template('viewcart.html', cart = cart_items)



@ecom.route('/viewcart')
@login_required
def viewCart():
    cart_items = Cart.query.all()[::-1]
    return render_template('viewcart.html', cart = cart_items)



@ecom.route('/cart/delete/<int:post_id>', methods=["POST"]) # not a GET request because you are really just POSTing to delete
@login_required
def deleteIndCart(post_id):
    cart = Cart.query.filter_by(id=post_id).first()
    if cart is None:
        return redirect(url_for('ecom.posts'))
    if cart.user_id != current_user.id:
        return redirect(url_for('ecom.posts'))

    # for 
    db.session.delete(cart)
    db.session.commit()     
    return redirect(url_for('ecom.cart')) # staying in the cart