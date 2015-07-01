from elections.views import SoulMateDetailView
from votai_theme.calculator import YQSCalculator
from django.http import JsonResponse
from candidator.models import TakenPosition


class MediaNaranjaView(SoulMateDetailView):
    calculator_class = YQSCalculator


class MedianaranjaJsonView(MediaNaranjaView):
    def dispatch(self, *args, **kwargs):
        super(MedianaranjaJsonView, self).dispatch(*args, **kwargs)
        election = self.object
        response = {
            'Id': election.id,
            "Nombre": election.name,
            "Distrito": election.area.name,
            "Nivel": election.extra_info['nivel'],
            "Cargo": election.extra_info['cargo'],
            "Preguntas": {
                "Id": 0,
                "Nro_Preguntas": 0,
                "Nro_Candidatos": 0,
                "Categorias": [],
                "Candidatos": []
            }

        }
        for category in election.categories.all():
            category_dict = {'category_id': category.slug,
                             'Texto': [],
                             'Opciones': []
                             }
            for topic in category.topics.all():
                question_dict = {"Id": topic.slug,
                                 "Texto": topic.label,
                                 "Opciones": []
                                 }
                response['Preguntas']["Nro_Preguntas"] += 1
                topic_positions = []
                for position in topic.positions.all():
                    position_dict = {"answer_id": position.id,
                                     "answer_text": position.label,
                                     "answer_value": position.answervalue.value
                                     }
                    topic_positions.append({
                        "Id": position.id,
                        "Texto": position.label})
                category_dict['Opciones'].append(topic_positions)
                # response['Preguntas']['Categorias'].append(question_dict)
                category_dict['Texto'].append(topic.label)
            response['Preguntas']['Categorias'].append(category_dict)
        response['Preguntas']["Nro_Candidatos"] = election.candidates.count()
        for candidate in election.candidates.all():
            candidate_dict = {'Id': candidate.id,
                              'Nombre': candidate.name,
                              'Foto': candidate.image,
                              }
            taken_positions = TakenPosition.objects.filter(position__topic__category__in=election.categories.all(), person=candidate)
            for taken_position in taken_positions:
                taken_position_dict = {'question_id': taken_position.topic.id,
                                       'answer_id': taken_position.position.id
                                       }
                if taken_position.topic.category.slug not in candidate_dict.keys():
                    candidate_dict[taken_position.topic.category.slug] = []
                candidate_dict[taken_position.topic.category.slug].append(taken_position.position.id)
            response['Preguntas']['Candidatos'].append(candidate_dict)
        return JsonResponse(response)
