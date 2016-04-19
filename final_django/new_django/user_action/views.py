from django.shortcuts import render, get_object_or_404 , redirect
# Create your views here.
from django.http import HttpResponse
from articles.models import *
from .forms import PostForm , CommentForm , ReplyForm



def profile(request,user_id):
    # user = User.objects.get(pk=request.session['user_id'])
    user = User.objects.get(pk=user_id)
    show_img=User_profile.objects.get(pk=user_id)
    image=str(show_img.user_img)[2:]
    # return HttpResponse(image)
    # output = '<ul>'
    # output += '<li>'+user.username+'</li>'
    # output += '<li>'+user.password+'</li>'
    # output += '<li>'+str(show_img.user_img)+'</li>'
    # output += '</ul>'
    context={
       'user':user,
       'image':image
    }
    return render(request,'user_action/profile.html',{'context':context})



def system_locked(request):
    return render(request,'user_action/system_locked.html')




def home(request):
    lock = lockSystem.objects.get(pk=1)
    if lock.is_locked == True:
        return redirect("http://127.0.0.1:8000/user_action/system_locked") 
    else:
        top_article_list = Article.objects.order_by('-art_number_views')[:3]
        images = []
        for article in top_article_list:
            images.append(article.art_img.name[11:])
        # return HttpResponse(images[0])
        context = {
            'top_article_list': top_article_list,
            'images':images
        }
        return render(request, 'user_action/home.html', context)


def index(request):
    user  = User.objects.get(pk=request.session['user_id'])
    # marks = Mark.objects.filter(request.session['user_id'])
    # return HttpResponse()
    if "user_id" in request.session:
        latest_article_list = Article.objects.order_by('art_publish_date')[:10]
        # return HttpResponse(request.session['user_id'])
        marked_articles = Mark.objects.filter(user_id=request.session['user_id'])
        context = {
            'latest_article_list': latest_article_list,
            'marked_articles':marked_articles,
            'user':user
        }
        return render(request, 'user_action/index.html', context)
    else:
        return redirect('http://127.0.0.1:8000/user_action/home')


def design(request):
	return render(request,'user_action/index1.html')


def mark(request):
    if request.GET.get('mark'):
       # article = Article.objects.get(pk=request.GET.get('article_id'))
       mark = Mark()
       mark.user_id = request.GET.get('user_id')
       mark.article_id = request.GET.get('article_id')
       mark.save()
       return HttpResponse("may be yes and may be no")
    else:
       mark = Mark.objects.get(user_id=request.GET.get('user_id'),article_id=request.GET.get('article_id'))
       mark.delete()
       return HttpResponse("may be yes and may be no")


def like(request):
    # return HttpResponse("comment")
    # return HttpResponse("comment")
    if request.GET.get('like') == 'yes':
        if request.GET.get('comment_id') and request.GET.get('user_id'):
    	    # comment=Comment()
            comment = Comment.objects.get(pk=request.GET.get('comment_id'))
            # user = Obj_user.objects.get(pk=request.GET.get('user_id'))
            # comment.user_set.add(user)
            comment.Comment_user_like.add(User.objects.get(pk=request.GET.get('user_id')))
            return HttpResponse("may be yes and may be no")
    else:
        if request.GET.get('comment_id') and request.GET.get('user_id'):
           # comment=Comment()
           comment = Comment.objects.get(pk=request.GET.get('comment_id'))
           # user = Obj_user.objects.get(pk=request.GET.get('user_id'))
           # comment.user_set.add(user)
           comment.Comment_user_like.remove(User.objects.get(pk=request.GET.get('user_id')))
           return HttpResponse("may be yes and may be no")



def details(request, article_id):
    try:
        user = User.objects.get(pk=request.session['user_id'])
        form1 = ReplyForm()
        article = Article.objects.get(pk=article_id)
        if article.art_status == 'p':
            keywords = article.keywords_set.all()
            related_articles = []
            related_articles = Article.objects.filter(keywords__in=keywords)
            # for key in keywords:
            #     related_articles.append(key.related.all())
            # item_list = Item.objects.filter(committees__in=committee_relations)
            # return HttpResponse(related_articles)
            article.art_number_views += 1
            article.save()
            artimage = article.art_img.name[11:]
            # return HttpResponse(artimage)
            if request.POST.get('comment'):
                form = CommentForm(request.POST)
                if form.is_valid():
                    comment = Comment()
                    banned_words = Banwords.objects.all()
                    filtered_comment = form.cleaned_data['comment']
                    for banned in banned_words:
                        filtered_comment=filtered_comment.replace(banned.banword_name,"***")
                        # return HttpResponse(filtered_comment)
                    comment.Comment_content = filtered_comment
                    comment.Comment_art_id_id = article_id
                    comment.Comment_parent_id = -1
                    comment.save()

            if request.POST.get('reply'):
                form1 = ReplyForm(request.POST)
                if form1.is_valid():
                    # return HttpResponse('da5al')
                    reply = Comment()
                    banned_reply = Banwords.objects.all()
                    reply.Comment_content = form1.cleaned_data['reply']
                    for banned in banned_reply:
                        reply.Comment_content=reply.Comment_content.replace(banned.banword_name,"***")
                    
                    reply.Comment_art_id_id = article_id
                    reply.Comment_parent_id = form1.cleaned_data['parentcomment']

                    reply.save()

            comments = article.comment_set.all()
            # return HttpResponse(comments)
            	# comment.comment_set.all()       
            	# get_object_or_404(Comment,Comment_parent_id=comment.id)
            context = {"article":article,"comments":comments,"form":form1,"artimage":artimage,"related_articles":related_articles,"user":user}
            return render(request,'user_action/details.html',context)
        else:
            return redirect("http://127.0.0.1:8000/user_action/")
    except Article.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'user_action/details.html', context)



def addBlog(request):
    user = User.objects.get(pk=request.session['user_id'])
    if request.GET.get('id'):
        article_id = request.GET.get('id')
        article = Article.objects.get(pk=article_id)
        context = {"article":article, "user":user}
        return render(request,'user_action/addBlog.html',context)
    else:
        context = {"user":user}
        return render(request,'user_action/addBlog.html',context)


def success(request):	
    if request.method =="POST":
        if request.GET.get('id'):
            article_id = request.GET.get('id')
            article = Article.objects.get(pk=article_id)
            form = PostForm(request.POST, request.FILES)

            if form.is_valid():
                # return HttpResponse("ok")
                article.art_title = form.cleaned_data['title']
                article.art_content = form.cleaned_data['content']
                article.art_img =form.cleaned_data['image']
                article.save()
            # return render(request,'user_action/success.html')
            return redirect('http://127.0.0.1:8000/user_action/')
        else:
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                article = Article()
                article.art_title = form.cleaned_data['title']
                article.art_content = form.cleaned_data['content']
                article.art_img = form.cleaned_data['image']
                article.art_user_id_id = request.session['user_id']
                article.save()
            # return render(request,'user_action/success.html')
            return redirect('http://127.0.0.1:8000/user_action/')

    if request.GET.get('action'):
        if request.GET.get('id'):
            article_id = request.GET.get('id')
            article = Article.objects.get(pk=article_id)
            article.delete()
        # return render(request,'user_action/success.html')
        return redirect('http://127.0.0.1:8000/user_action/')