# Использование APIView Tracker
___
## Описание
APIView - это базовое представление, которое предоставляет вам DRF, аналогично дженерикам Django. Оно отличается от обычного View тем, что использует собственные объекты Request и Response вместо джанговских, которые сразу умеют сериализовывать данные, а также некоторыми настройками, специфичными для DRF.

## Serializer
Модельный сериализатор - это сериализатор на базе встроенного класса ModelSerializer.
```angular2html
class TrackerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tracker
        fields = ['id', 'summary', 'description', 'created_at', 'updated_at']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'start_date', 'end_date']
```

## TrackerDetailView
Представление детального просмотра
```
class TrackerDetailView(APIView):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        serializer_project = ProjectSerializer(project)
        tracker = Tracker.objects.filter(project_id=pk)
        serializer = TrackerSerializer(tracker, many=True)
        data = {'project': serializer_project.data, 'tracker': serializer.data}
        return Response(data, status=status.HTTP_200_OK)
```
## URL 
url путь передаем pk для просмотра **одной записи**
```angular2html
path('tracker/<int:pk>/', TrackerDetailView.as_view(), name='detail_traker')
```
# Postman
Пример запроса:
```angular2html
GET http://127.0.0.1:8000/api/tracker/1
```
Ответ:
```angular2html
{
    "project": {
        "id": 1,
        "name": "Project 1",
        "description": "Project number 1",
        "created_at": "2023-04-17T06:20:32.849192Z",
        "updated_at": "2023-04-18T07:32:43.314719Z",
        "start_date": "2023-05-01",
        "end_date": "2023-05-31"
    },
    "tracker": [
        {
            "id": 3,
            "summary": "Task 1",
            "description": "Task numeber 1",
            "created_at": "2023-04-17T06:22:52.225171Z",
            "updated_at": "2023-04-17T15:35:34.500776Z"
        },
        {
            "id": 8,
            "summary": "Task 6",
            "description": "Task number 6",
            "created_at": "2023-04-18T03:37:30.620006Z",
            "updated_at": "2023-04-18T03:37:30.620031Z"
        },
        {
            "id": 12,
            "summary": "Task 10",
            "description": "Task number 10",
            "created_at": "2023-04-18T03:39:17.606031Z",
            "updated_at": "2023-04-18T03:39:17.606058Z"
        }
    ]
}
```
Пример запроса при несуществующим id:
```angular2html
GET http://127.0.0.1:8000/api/tracker/19
```
Ответ:
```angular2html
{
    "detail": "Not found."
}
```
## TrackerDeleteView
Представление удаления
```
class TrackerDetailView(APIView):
        def delete(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        tracker = Tracker.objects.filter(project_id=pk)
        tracker.delete()
        project.delete()
        return Response({'pk': pk}, status=status.HTTP_204_NO_CONTENT)
```
## URL
```angular2html
path('tracker/delete/<int:pk>/', TrackerDeleteView.as_view(), name='delete_tracker')
```
# Postman
Пример запроса: 
```angular2html
DELETE  http://127.0.0.1:8000/api/tracker/delete/2/
```
Ответ возвращает ключ:
```angular2html
{
    "pk": 2
}
```
В случае неправильного запроса:
```angular2html
{
    "detail": "Not found."
}
```
## TrackerUpdateView
Представление редактирования
```
class TrackerUpdateView(APIView):

    def put(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        tracker = Tracker.objects.filter(project_id=pk)
        serializer_project = ProjectSerializer(project, data=request.data)
        if serializer_project.is_valid():
            serializer_project.save()
        else:
            return Response(serializer_project.errors, status=400)
        serializer = TrackerSerializer(tracker, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
```
## URL
```angular2html
path('tracker/update/<int:pk>/', TrackerUpdateView.as_view(), name='update_tracker')
```
# Postman
Пример запроса: 
```angular2html
PUT  http://127.0.0.1:8000/api/tracker/update/2/
```
raw(JSON):
```angular2html

{
    "name": "Project 1",
    "description": "Project number 1",
    "start_date": "2023-05-01",
    "end_date": "2023-05-31"
}
```
Ответ:
Поменяются значения project</br>
В случае неправильного запроса:
```angular2html
{
    "detail": "Not found."
}
```
