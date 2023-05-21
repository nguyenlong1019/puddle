from django.shortcuts import render, get_object_or_404, redirect
from item.models import Item
from .models import Conversation
from .forms import ConversationMessageForm
from django.contrib.auth.decorators import login_required

@login_required
def new_conversation(request, item_pk):
    """
    item_pk là primary key for item
    """
    item = get_object_or_404(Item, pk=item_pk)

    # trong django request.user đại diện cho đối tượng hiện tại đang thực hiện hành động trên website
    if item.created_by == request.user:
        # có thể chuyến hướng người dùng đến bất cứ đâu bạn muốn nếu sản phẩm do chính người đang dùng tạo ra
        return redirect('dashboard:index')
    
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

    if conversations:
        pass # redirect to conversation

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)   # add customer
            conversation.members.add(item.created_by)  # add seller
            conversation.save()

            conversation_messages = form.save(commit=False)
            conversation_messages.conversation = conversation
            conversation_messages.created_by = request.user
            conversation_messages.save()

            return redirect('item:detail', pk=item_pk)
        
    else:
        form = ConversationMessageForm()
    
    return render(request, 'conversation/new.html', {
        'form': form,
    })

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    # print(conversations)

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations,
    })

@login_required
def detail(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    print(conversation)

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
    })