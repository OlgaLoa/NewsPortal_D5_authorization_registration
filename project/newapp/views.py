# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД

#ListView:запрашивает данные из базы по указанной модели, находит указанный шаблон,
#передаёт объекты в шаблон. При этом у него есть методы, которые мы можем переопределить.
#Одним из таких методов является get_context_data, позволяет нам получить дополнительные данные,
#которые будут переданы в шаблон.

from datetime import datetime

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import NewsFilter
from .forms import NewsForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin


class NewsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news_list.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news_list'
    paginate_by = 10  # вот так мы можем указать количество записей на странице

class NewsDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'news_detail.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'news_detail'

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        return context

class NewsSearch(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news_search.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news_search'
    paginate_by = 10  # вот так мы можем указать количество записей на странице

    #Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = NewsFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class NewsCreate(PermissionRequiredMixin,CreateView):# Добавляем новое представление для создания новости.
    permission_required = ('newapp.add_post',) #add_post из админки Chosen permissions
    form_class = NewsForm # Указываем нашу разработанную форму
    model = Post # модель
    template_name = 'news_create.html' #новый шаблон, в котором используется форма.
    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news/news/create/': # в модели Post categoryType по default = Article
            post.categoryType = 'NW' #если вызывается этот путь - сохраняется как NW
        post.save() #сохраняем форму
        return super().form_valid(form)

class NewsUpdate(PermissionRequiredMixin, UpdateView):# Добавляем новое представление для создания новости.
    permission_required = ('newapp.change_post',)
    form_class = NewsForm # Указываем нашу разработанную форму
    model = Post # модель
    template_name = 'news_update.html' # и новый шаблон, в котором используется форма.
#
class NewsDelete(PermissionRequiredMixin, DeleteView):# Добавляем новое представление для создания новости.
    permission_required = ('newapp.delete_post',)
    model = Post # модель
    template_name = 'news_delete.html' # и новый шаблон, в котором используется форма.
    success_url = reverse_lazy('news_list')# куда перенеправить поль-ля после удаления товара
