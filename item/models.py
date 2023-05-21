from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',) # thêm dấu , vì đây là một iterable
        verbose_name_plural = 'Categories'
        # dùng để đặt lại tên model trong item app vì mặc định khi tên model là Category
        # django sẽ tự động thêm s trở thành Categorys, như này là sai chính tả

    def __str__(self):
        return self.name

class Item(models.Model):
    """
    name: tên sản phẩm
    description: mô tả sản phẩm, có thể blank nếu người dùng không muốn cung cấp mô tả cho sản phẩm
    price: giá
    is_sold: là kiểm tra xem sản phẩm có được bán hay không? mặc định là False
    created_by: được tạo bởi ai: điều này là một index trong database giữa item và user
    on_delete: nếu người dùng (user) bị xóa thì tất cả items cũng sẽ bị xóa
    """
    # khi một trường foreign key được định nghĩa, nó thực sự tự tạo ra một trường trong CSDL
    # với mẫu: <field_name>_id => category là foreignkey nên sẽ tự tạo ra category_id
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name