from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Category
from .forms import NewItemForm, EditItemForm
from django.db.models import Q

def items(request):
    # tham số thứ nhất là value: query, tham số thứ hai là giá trị mặc định
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0) # lấy giá trị category trong URL request GET
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id:
        # lọc với field là category_id
        items = items.filter(category_id=category_id)

    if query:
        # tìm kiếm chuỗi chứa query không phân biệt chữ hoa chữ thường
        # icontains = insensitive contains
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id),
    })

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]
    # lấy 3 sản phẩm liên quan, chưa bán và không bao gồm item

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items,
    })

# khi chưa đăng nhập mà bấm vào new item thì sẽ ra login
@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False) # commit = False vì chưa có trường created_by nên chưa commit
            # dòng trên chỉ tạo đối tượng mà chưa lưu nó trong database

            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New Item',
    })

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect('item:detail', pk=item.id)
    else:
        # cung cấp data vào form để edit
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit Item',
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard:index')