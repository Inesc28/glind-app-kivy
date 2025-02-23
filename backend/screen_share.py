import socket
import json
from PIL import Image
from jnius import autoclass, cast
import numpy as np
import io
import base64

# Clases de Android
PythonActivity = autoclass('org.kivy.android.PythonActivity')
Context = autoclass('android.content.Context')
MediaProjectionManager = autoclass('android.media.projection.MediaProjectionManager')
BitmapFactory = autoclass('android.graphics.BitmapFactory')
ByteArrayOutputStream = autoclass('java.io.ByteArrayOutputStream')
Bitmap = autoclass('android.graphics.Bitmap')
ImageReader = autoclass('android.media.ImageReader')
VirtualDisplay = autoclass('android.hardware.display.VirtualDisplay')

# Captura de pantalla usando MediaProjection
def capture_and_send_frames(user_id, target_user_id, server_ip, server_port):
    activity = PythonActivity.mActivity
    mpm = activity.getSystemService(Context.MEDIA_PROJECTION_SERVICE)
    intent = activity.getIntent()
    projection = mpm.getMediaProjection(intent.getIntExtra('code', -1), intent.getParcelableExtra('data'))
    
    width, height = 720, 1280
    image_reader = ImageReader.newInstance(width, height, Bitmap.Config.ARGB_8888, 2)
    virtual_display = projection.createVirtualDisplay("screen-share",
                                                    width, height, 320,
                                                    VirtualDisplay.FLAG_PUBLIC,
                                                    image_reader.getSurface(), None, None)
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    try:
        while True:
            image = image_reader.acquireLatestImage()
            if image:
                planes = image.getPlanes()
                buffer = planes[0].getBuffer()
                width = image.getWidth()
                height = image.getHeight()
                pixel_stride = planes[0].getPixelStride()
                row_stride = planes[0].getRowStride()
                row_padding = row_stride - pixel_stride * width
                bitmap = Bitmap.createBitmap(width + row_padding // pixel_stride, height, Bitmap.Config.ARGB_8888)
                bitmap.copyPixelsFromBuffer(buffer)
                
                stream = ByteArrayOutputStream()
                bitmap.compress(Bitmap.CompressFormat.JPEG, 100, stream)
                byte_array = stream.toByteArray()
                frame_data = base64.b64encode(byte_array).decode()
                image.close()
                
                message = {
                    "action": "screen_frame",
                    "userId": user_id,
                    "targetUserId": target_user_id,
                    "frame": frame_data
                }
                client_socket.sendall(json.dumps(message).encode())
    except Exception as e:
        print(f"Error al capturar y enviar frames: {e}")
    finally:
        virtual_display.release()
        client_socket.close()

def receive_and_display_frames(user_id, server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    try:
        while True:
            data = client_socket.recv(4096).decode()
            if not data:
                break
            frame_data = json.loads(data).get("frame")
            np_frame = np.frombuffer(base64.b64decode(frame_data), dtype=np.uint8)
            frame = Image.open(io.BytesIO(np_frame))
            frame.show()  # Esto es solo un ejemplo, debes mostrar el frame en un widget Kivy
    except Exception as e:
        print(f"Error al recibir y mostrar frames: {e}")
    finally:
        client_socket.close()