from django.db import models

#    def get_absolute_url(self):
#        return reverse("video_detail", kwargs = {"pk":self.pk})

class Video(models.Model):
        title = models.CharField(max_length = 100)
        description = models.TextField()
        file = models.FileField(upload_to= 'static/video/')
        poster = models.FileField(upload_to= 'static/poster/')

        def str (self):
            return self.title

        class Meta:
            verbose_name = "Video"
            verbose_name_plural = "Video"


class Client(models.Model):
        client_id = models.CharField(max_length = 100)

        def str (self):
            return self.client_id

        class Meta:
            verbose_name = "Cliente"
            verbose_name_plural = "Clienti"


class Emotion(models.Model):
        client = models.ForeignKey(Client, on_delete = models.CASCADE)
        video_id = models.IntegerField()
        titleV = models.CharField(max_length = 100)


        response = models.CharField(max_length = 100)
        time = models.CharField(max_length = 100)
        sequence = models.IntegerField();


        def str (self):
            return str(self.client)

        class Meta:
            verbose_name = "Emozione"
            verbose_name_plural = "Emozioni"

class Statistics(models.Model):
        video_id = models.IntegerField()

        arrabbiato = models.IntegerField(default= 0)
        felice =models.IntegerField(default= 0)
        triste =models.IntegerField(default= 0)
        disgustato = models.IntegerField(default= 0)
        sorpreso = models.IntegerField(default= 0)
        annoiato = models.IntegerField(default= 0)
        impaurito = models.IntegerField(default= 0)

        sequence = models.CharField(max_length = 100);


        def str (self):
            return str(self.video_id)

        class Meta:
            verbose_name = "Statistiche"
            verbose_name_plural = "Statistiche"
