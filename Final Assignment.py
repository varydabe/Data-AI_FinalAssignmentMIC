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
            label_positif = Label(root, text="SUSPECTED POSITIVE")
            label_positif.grid(row=7, column=2)
    else:
            label_negatif = Label(root, text="SUSPECTED NEGATIVE")
            label_negatif.grid(row=7, column=2)

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
root.title("Covid-19 Suspect Prediction")

#widget label, button, and entry
label_header = Label(root, text="This app will predict your status based on these three variable")
label_wkt = Label(root, text="Time spend with other people(minutes):")
entry_wkt = Entry(root)
label_jml = Label(root, text="Number of people interaction:")
entry_jml = Entry(root)
label_suhu  = Label(root, text="Body temperature(°C):")
entry_suhu = Entry(root)

button_prd = Button(root, text="Predict", command=printPredict)

label_hasil  = Label(root, text="Based on predict with Machine learning, your status is")
label_ext  = Label(root, text="It is recommended to conduct further tests at a health facility")

#calling the widget obj and position
label_header.grid(columnspan=3)
label_wkt.grid(row=2, column=1, sticky=E)
entry_wkt.grid(row=2, column=2, sticky=W)
label_jml.grid(row=3, column=1,sticky=E)
entry_jml.grid(row=3, column=2, sticky=W)
label_suhu.grid(row=4, column=1,sticky=E)
entry_suhu.grid(row=4, column=2, sticky=W)

button_prd.grid(columnspan=3)

label_hasil.grid(row=7, column=1)
label_ext.grid(columnspan=3)

#calling the root to loop until the window closed
root.mainloop()
