# first-neural-network
Neural network that recognizes drawn digits

### How to Use
1. Run *paint.py* to draw ten digits (0-9) and save each as a png file.
2. Run *neural_network.py* to train a network with *training_data.csv* and test it with the images created in step 1.

### Additional Information
Node outputs are defined by a logistic/sigmoid activation function.

This program was written in Python 3.7 and requires the third-party modules *NumPy*, *Pillow*, and *imageio*.

The file *training_data.csv* contains the data of 340 28x28 images (34 for each digit), turned into csv using the following code:

    for i in range(len(os.listdir(os.path.join(os.getcwd(), 'train')))):
      image_path = os.path.join(os.getcwd(), 'train/{num}.png'.format(num=i))
      image = imageio.imread(image_path)
      image = 255.0 - image.flatten()
      image = image / 255.0 * 0.99 + 0.01
      image = list(str(i)[-1]) + list(image) # adds current digit in front
        # assumes that files are decadically ordered (e.g., image file #24 represents digit 4)
      with open('training_data.csv', 'a', newline='') as file:
        writer_object = csv.writer(file, delimiter=',')
        writer_object.writerow(image)
