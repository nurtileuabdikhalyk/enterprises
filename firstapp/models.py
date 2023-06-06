from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    name = models.CharField('Тауар аты', max_length=150)
    price = models.IntegerField('Бағасы')
    count = models.IntegerField('Саны')
    organization = models.ForeignKey(User, default=User, verbose_name='Мекеме', on_delete=models.CASCADE)

    place = models.CharField('Орналасқан орны', max_length=255)

    @property
    def total(self):
        return self.price * self.count

    class Meta:
        verbose_name = "Тауар"
        verbose_name_plural = "Тауарлар"

    def __str__(self):
        return f"{self.name} - {self.price} ₸"


class Feedback(models.Model):
    fullname = models.CharField('Аты-жөні', max_length=255)
    message = models.TextField('Пікір')
    image = models.ImageField('Сурет', upload_to='image/', blank=True, null=True)
    created = models.DateTimeField('Уақыты', auto_now_add=True)

    class Meta:
        verbose_name = "Пікір"
        verbose_name_plural = "Пікірлер"

    def __str__(self):
        return self.fullname


class Contact(models.Model):
    first_name = models.CharField('Есімі', max_length=150)
    last_name = models.CharField('Тегі', max_length=150, blank=True, null=True)
    email = models.EmailField('Почта')
    subject = models.CharField('Тақырыбы', max_length=150, blank=True, null=True)
    message = models.TextField('Хабарлама')
    created = models.DateTimeField('Уақыты', auto_now_add=True)

    class Meta:
        verbose_name = "Сұрақ"
        verbose_name_plural = "Сұрақтар"

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.subject}"


class Dogovor(models.Model):
    name = models.CharField('Келісім-шарт', max_length=150)
    description = models.TextField('Сипаттама', blank=True, null=True)
    organization = models.ForeignKey(User, default=User, verbose_name='Мекеме', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Келісім-шарт'
        verbose_name_plural = 'Келісім-шарттар'

    def __str__(self):
        return f"{self.name}"


class Project(models.Model):
    name = models.CharField('Жоба аты', max_length=150)
    description = models.TextField('Сипаттама', blank=True, null=True)
    organization = models.ForeignKey(User, default=User, verbose_name='Мекеме', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Жоба'
        verbose_name_plural = 'Жобалар'

    def __str__(self):
        return f"{self.name}"


class Platej(models.Model):
    OPLATA_CHOICE = (
        ('Карта', 'Карта'),
        ('Қолма-қол', 'Қолма-қол'),
        ('QR-код', 'QR-код'),
    )
    STATUS_CHOICE = (
        ('Төленді', 'Төленді'),
        ('Төленбеді', 'Төленбеді'),
    )
    organization = models.ForeignKey(User, verbose_name='Мекеме', on_delete=models.CASCADE)
    dogovor = models.ForeignKey(Dogovor, verbose_name='Келісім-шарт', on_delete=models.CASCADE)
    # project = models.ForeignKey(Project, verbose_name='Жоба', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Тауар', on_delete=models.CASCADE)
    oplata = models.CharField('Төлем түрі', max_length=150, choices=OPLATA_CHOICE)
    address = models.CharField('Мекен-жай', max_length=150)
    status = models.CharField('Төленді/Төленбеді', max_length=150, choices=STATUS_CHOICE)
    count = models.IntegerField('Саны', default=1, blank=True, null=True)
    sum = models.DecimalField('Сумма', max_digits=12, decimal_places=2)
    ndc = models.DecimalField('НДС', max_digits=9, decimal_places=2, blank=True, null=True)

    @property
    def profit(self):
        return self.sum * self.count - self.product.price * self.count - self.ndc

    class Meta:
        verbose_name = 'Сатылым'
        verbose_name_plural = 'Сатылымдар'

    def save(self, *args, **kwargs):
        self.ndc = self.sum * 12 * self.count / 100
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} {self.product.name} {self.sum}"


class Order(models.Model):
    organization = models.ForeignKey(User, verbose_name='Мекеме', on_delete=models.CASCADE)
    data = models.DateTimeField('Уақыты')
    platej = models.ForeignKey(Platej, verbose_name='Сатылым', on_delete=models.CASCADE, blank=True, null=True)
    courier = models.ForeignKey('Courier', verbose_name='Жоба', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Тапсырыс'
        verbose_name_plural = 'Тапсырыстар'

    def __str__(self):
        return f"{self.id} {self.platej} {self.data}"


class Notes(models.Model):
    title = models.CharField("Тақырыбы", max_length=255, blank=True, null=True)
    description = models.TextField("Сипаттама")
    organization = models.ForeignKey(User, default=User, verbose_name='Мекеме', on_delete=models.CASCADE)
    created = models.DateTimeField("Құрылған уақыты", auto_now_add=True)

    class Meta:
        verbose_name = "Ескертпе"
        verbose_name_plural = "Ескертпелер"

    def __str__(self):
        return f"{self.id} {self.title} {self.created}"


class Courier(models.Model):
    organization = models.ForeignKey(User, verbose_name='Мекеме', on_delete=models.CASCADE)
    first_name = models.CharField('Есімі', max_length=150)
    last_name = models.CharField('Тегі', max_length=150)
    phone = models.CharField('Телефон', max_length=16)

    class Meta:
        verbose_name = "Курьер"
        verbose_name_plural = "Курьер"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
