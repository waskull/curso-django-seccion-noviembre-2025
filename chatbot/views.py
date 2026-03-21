from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from chatbot.models import Conversacion
from chatbot.serializers import ConversacionSerializer
from chatbot.rag import generar_respuesta
from inventario.models import Producto


class ChatbotView(APIView):
    serializer_class = ConversacionSerializer
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        engine = request.query_params.get('engine', "llamacpp").lower()
        pregunta = serializer.validated_data["pregunta"].lower()

        productos = Producto.objects.all()
        contexto = "\n".join(
            [f"Producto: {p.nombre.lower()} | Descripcion: {p.descripcion.lower()} | Precio: {p.precio} | Cantidad: {p.cantidad} | Categoria: {p.categoria.nombre.lower()}" for p in productos])

        SYSTEM_PROMPT = (
            "Eres el asistente del sistema eCommerce llamado BodeGON. "
            "Usa solo la información provista en el 'CONTEXT' para responder "
            "consultas sobre productos, disponibilidad del stock y productos mas vendidos. "
            "Si no puedes responder con la información disponible, indica que no puedes responder."
        )
        prompt = (
            f"{SYSTEM_PROMPT}\n\n"
            f"=== CONTEXT ===\n{contexto}\n\n"
            "=== INSTRUCCIÓN ===\n"
            "Responde solo con información del contexto. Sé claro, conciso y emite la respuesta en texto plano.\n"
        )
        temperatura = serializer.validated_data.get("temperatura", 0.7)
        modelo = serializer.validated_data.get("modelo", "modelo_base")
        try:
            print("Haciendo petición con el modelo:", modelo)
            print("Prompt:", prompt)
            print("Pregunta:", pregunta)
            print("Engine:", engine)
            respuesta = generar_respuesta(prompt,pregunta, temperatura=temperatura, engine=engine)
            print("Respuesta:", respuesta)
            LISTA_ERROR = ["No puedo responder a esa pregunta.",
                           "No puedo responder a tu pregunta.", "No puedo responder a tu pregunta", ""]
            if respuesta or respuesta not in LISTA_ERROR:
               print("Guardando conversacion")
               Conversacion.objects.create(pregunta=pregunta,respuesta=respuesta, usuario=request.user, temperatura=temperatura)
               return Response({"pregunta": pregunta, "respuesta": respuesta})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        return Response({"pregunta": pregunta, "respuesta": respuesta})
    
    def get(self, request):
        if request.user.is_authenticated:
            conversacion = Conversacion.objects.filter(
                usuario=request.user)
        else:
            conversacion = Conversacion.objects.all()[:10]
        serializer = ConversacionSerializer(conversacion, many=True)
        return Response(serializer.data)