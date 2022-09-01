from django.core.validators import RegexValidator
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

from django.db import models

# Create your models here.
from django.db.models import PositiveSmallIntegerField, CharField, EmailField, ForeignKey, SlugField, \
    DateTimeField, ManyToManyField, OneToOneField, BooleanField
from django.utils.text import slugify


class PhoneModel(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # Validators should be a list


class City(models.Model):
    city_name: CharField = models.CharField(max_length=16, blank=True, null=True)
    address: CharField = models.CharField(max_length=60, blank=True, null=True)
    zipcode: CharField = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        verbose_name = "Ville"


class PublisherHouse(models.Model):
    publishing_house_name: CharField = models.CharField(max_length=30)
    publisher_contact_mail: EmailField = models.EmailField()
    publisher_phone_number: PhoneModel = PhoneModel()
    publisher_location = models.ForeignKey(City, on_delete=models.CASCADE)


class DirectoryUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Vous devez entrer un email.")

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email=email, password=password)
        user.is_admin = True
        user.save()
        return user


class UserManagementSystem(AbstractBaseUser):
    email: EmailField = models.EmailField(
        unique=True,
        max_length=255,
        blank=True
    )
    is_active: BooleanField = models.BooleanField(default=True)
    is_admin: BooleanField = models.BooleanField(default=False)

    objects: DirectoryUserManager = DirectoryUserManager()

    USERNAME_FIELD: str = "email"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin


class BookCategory(models.Model):
    category_name: CharField = models.CharField(max_length=16)
    category_slug: SlugField = models.SlugField()

    class Meta:
        verbose_name = "Catégorie de livre"

    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        if not self.category_slug:
            self.category_slug = slugify(self.category_name)

        super().save(*args, **kwargs)


class Book(models.Model):
    book_title: CharField = models.CharField(max_length=16)
    book_author_name: CharField = models.CharField(max_length=16)
    book_reference: CharField | str = models.CharField(max_length=16)
    category_book: OneToOneField = models.OneToOneField(BookCategory, on_delete=models.SET_NULL, null=True)
    publisher_reference = models.ForeignKey(PublisherHouse, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Livre"

    def __str__(self):
        return self.book_title

    def save(self, *args, **kwargs):
        if not self.book_reference:
            self.hashed_title = hash(self.book_title)
            self.hashed_value_title = HashSet().hash_values(self.hashed_title)
            self.book_reference = f"{self.book_title[:3]}-{self.hashed_value_title}"

        super().save(*args, **kwargs)


class SocioProfessionnalCategory(models.Model):
    category_name_socio_professionnal: CharField = models.CharField(max_length=20, blank=True, null=True)
    category_code_socio_professionnal: CharField = models.CharField(max_length=20, blank=True, null=True)
    slug: SlugField = models.SlugField()

    class Meta:
        verbose_name = "Catégorie Socio-Professionnelle"

    def __str_(self):
        return self.category_name_socio_professionnal

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_socio_professionnal_category)

        super().save(*args, **kwargs)


class Client(models.Model):
    client_name: CharField = models.CharField(max_length=60)
    client_mail: EmailField = models.EmailField()
    client_phone_number: PhoneModel = PhoneModel()
    client_address: OneToOneField = models.OneToOneField(City, related_name="ville_et_adresse",
                                                         on_delete=models.CASCADE, null=True)
    client_reference_number: type[PositiveSmallIntegerField] = models.PositiveSmallIntegerField()
    socio_professionnal_category: ManyToManyField = models.ManyToManyField(SocioProfessionnalCategory)

    class Meta:
        verbose_name = "client"

    def __str__(self):
        return self.client_name

    def save(self, *args, **kwargs):
        if not client_reference_number:
            self.hashed_name_client = hash(self.name_client)
            self.client_reference_number = HashSet().hash_values(self.hashed_name_client)

        super().save(*args, **kwargs)


class ClientCard(models.Model):
    client_register_process: Client
    date_of_creation_card: object | DateTimeField = models.DateTimeField()
    date_of_expiry_card: object | DateTimeField = models.DateTimeField()
    client_card_reference: OneToOneField = models.OneToOneField(Client, related_name="reference_client",
                                                                on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "Carte adhérent"

    def __str__(self):
        return self.card_reference_number

    def save(self, *args, **kwargs):
        self.client_register_process = Client()
        if not self.date_of_creation_card:
            self.dt = datetime.datetime.now(timezone.utc())
            self.utc_time = self.dt.replace(tzinfo=timezone.utc)
            self.date_of_creation_card = self.utc_time.timestamp()
        if not self.date_of_expiry_card and self.date_of_creation_card is True:
            self.dt_expiry = self.datetime.datetime.now() + self.datetime.timedelta(days=365)
            self.utc_time_expiry = self.dt_expiry.replace(tzinfo=timezone.utc)
            self.date_of_expiry_card = self.utc_time_expiry.timestamp()

        super().save(*args, **kwargs)


class BorrowedBook(models.Model):
    book_borrowed: ForeignKey = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    client_reference: ForeignKey = models.OneToOneField(Client, on_delete=models.CASCADE, null=True)
    date_of_borrow: object | DateTimeField = models.DateTimeField()
    date_of_expected_return: object | DateTimeField = models.DateTimeField()
    date_of_effective_return = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Livres empruntés"

    def __str__(self):
        return self.book_borrowed

    def save(self, *args, **kwargs):
        if not self.date_of_borrow:
            self.dt_borrow = datetime.datetime.now(timezone.utc())
            self.utc_time_borrow = self.dt_borrow.replace(tzinfo=timezone.utc)
            self.date_of_borrow = self.utc_time.timestamp()
        if not self.date_of_expected_return and self.date_of_borrow is True:
            self.dt_expected_return = self.datetime.datetime.now() + self.datetime.timedelta(days=30)
            self.utc_time_expected_return = self.dt_expected_return.replace(tzinfo=timezone.utc)
            self.date_of_expected_return = self.utc_time_expiry.timestamp()


class Ordered(models.Model):
    ordered_book: ForeignKey = models.ForeignKey(Book, on_delete=models.CASCADE)
    ordered_to_publisher: ManyToManyField = models.ManyToManyField(PublisherHouse)
    number_of_books: PositiveSmallIntegerField = models.PositiveSmallIntegerField()
    date_of_creation_order: object | DateTimeField = models.DateTimeField(blank=True, null=True)
    date_of_expected_reception_after_order: object | DateTimeField = models.DateTimeField(blank=True, null=True)
    date_of_effective_return_after_order: object | DateTimeField = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Commande"

    def __str__(self):
        return self.ordered_book

    def save(self, *args, **kwargs):
        if not self.date_of_creation_order:
            self.dt = datetime.datetime.now(timezone.utc())
            self.utc_time = self.dt.replace(tzinfo=timezone.utc)
            self.date_of_creation_order = self.utc_time.timestamp()
        if not self.date_of_excpected_reception_after_order and self.date_of_creation_order is True:
            self.dt_expected_reception = self.datetime.datetime.now() + self.datetime.timedelta(days=10)
            self.utc_time_expected_reception = self.dt_expected_reception.replace(tzinfo=timezone.utc)
            self.date_of_expected_reception_after_order = self.utc_time_expected_reception.timestamp()
        if self.date_of_expected_reception_after_order is not self.date_of_effective_return_after_order:
            self.send_email_to_publisher = EmailService(PublisherHouse.publisher_contact_mail)

        super().save(*args, **kwargs)


class Archive(models.Model):
    ongoing_order: Ordered
    book_reference: ForeignKey = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    archive_stock: PositiveSmallIntegerField = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "Archive"

    def save(self, *args, **kwargs):
        if not self.archive_stock:
            self.ongoing_order = Ordered()
            if self.datetime.now() is self.date_of_expected_reception_after_order:
                self.archive_stock += self.number_of_books
