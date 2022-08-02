from imgUp.models import Img 
from imgUp.models import Detection
from imgUp.models import Prediction

print("y")
all_det = Detection.objects.all()
c = 0

for det in all_det:
    # if c > 3:
    #     break
    det.img_name = None

    print(det.img_data)
    print(type(det.img_data))
    det.save()
    
    # c += 1


all_prediction = Prediction.objects.all()
for pre in all_prediction:
    img = pre.img
    img.pred_num = pre.pred_num
    img.save()
