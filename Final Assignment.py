#Varyd Abe - Microsoft Imagine Community 2020
from tkinter import *


 #predict func       
def printPredict():
    #getting input from entry
    wkt = entry_wkt.get()
    jml = entry_jml.get()
    suhu = entry_suhu.get()

    #using ml func to predict
    hasil = ml(wkt, jml, suhu)

    #if else func to give result    
    if hasil==1:
            label_positif = Label(root, text="POSITIF")
            label_positif.grid(row=5, column=2)
    else:
            label_negatif = Label(root, text="NEGATIF")
            label_negatif.grid(row=5, column=2)

#machine learning func, kNN algorithm
def ml(wkt, jml, suhu):
    import numpy as np
    import pandas as pd

    #getting dataset
    dataset = pd.read_csv('dataset-covid.csv')
    dataset = dataset.replace(to_replace =['Ya', 'Tidak'],  value = [1, 0])

    #x and y
    x = dataset.iloc[:, [1,2,3]].values
    y = dataset.iloc[:, -1].values

    #split between train and test data
    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.20, random_state = 0)

    #scaling the input before training
    from sklearn.preprocessing import StandardScaler
    sc = StandardScaler()
    x_train = sc.fit_transform(x_train)
    x_test = sc.transform(x_test)

    #training data
    from sklearn.neighbors import KNeighborsClassifier
    classifier = KNeighborsClassifier(n_neighbors = 5, metric = 'minkowski', p = 2)
    classifier.fit(x_train, y_train)

    #predic using kNN and return the values 1 or 0
    return(classifier.predict(sc.transform([[wkt, jml, suhu]])))

#call the interface func
root=Tk()

#window func, title and resizeable
root.resizable(FALSE,FALSE)
root.title("Aplikasi prediksi infeksi COVID-19")

#widget label, button, and entry
label_header = Label(root, text="Aplikasi prediksi infeksi COVID-19")
label_wkt = Label(root, text="Lama waktu berada diluar ruangan(menit):")
entry_wkt = Entry(root)
label_jml = Label(root, text="Jumlah orang yang ditemui:")
entry_jml = Entry(root)
label_suhu  = Label(root, text="Suhu tubuh:")
entry_suhu = Entry(root)

button_prd = Button(root, text="Prediksi", command=printPredict)

label_hasil  = Label(root, text="Menurut prediksi, kondisi Anda adalah")
label_ext  = Label(root, text="Disarankan untuk melakukan pemeriksaan lebih lanjut di fasilitas kesehatan")

#calling the widget obj and position
label_wkt.grid(row=1, column=1, sticky=E)
entry_wkt.grid(row=1, column=2)
label_jml.grid(row=2, column=1,sticky=E)
entry_jml.grid(row=2, column=2)
label_suhu.grid(row=3, column=1,sticky=E)
entry_suhu.grid(row=3, column=2)

button_prd.grid(columnspan=4)

label_hasil.grid(row=5, column=1)
label_ext.grid(columnspan=4)

#calling the root to loop until the window closed
root.mainloop()
