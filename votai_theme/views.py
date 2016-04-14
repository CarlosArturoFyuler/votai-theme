from elections.views import SoulMateDetailView


class MediaNaranjaView(SoulMateDetailView):
    def get_information_holder(self, data={}):
        holder = super(MediaNaranjaView, self).get_information_holder(data)
        return holder
