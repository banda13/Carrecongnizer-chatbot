_This project is part of my Carrecognizer-project group and was developed as a part of my master thesis at the Budapest University of Technology and Economics._

***
# Goal
My task was to design and implement a deep convolutional neural network-based application, which is able to recognize several features of a vehicle based on a picture, mainly the make and the model. Furthermore, I had to develop an application that allows the users to use the functionality of this model conveniently and easily. Based on this, my
work can be divided into two main parts:

The first stage involved doing research tasks as, so far there has been no good
solution, so my task was to plan and implement the whole process from the initial steps
to the birth of the trained model. In this section, I will introduce methods such as creating
WebCrawlers that process unstructured data from websites to build big data databases
with low resource requirements, preprocessing steps with pre-trained neural networks,
knowledge transfer (transfer train) on convolutional networks and various self-designed
evaluation algorithms. To solve these tasks, I had to try different techniques, combine
different approaches, and evaluate the results. Many of my attempts have not been
successful, but in the end, I managed to create a model that can perform this task with
sufficient accuracy.

The second part covers engineering tasks in the traditional sense with all their
challenges. These include the design and the development of a well-scalable, secure
backend and database that can quickly serve the requests of the clients and leverage the
capabilities of the neural model. The clients for the application would allow the users to
use the features conveniently and easily. In order to attract a larger userbase an Angular
based web client, an Android application written in Kotlin and a Facebook chatbot were
also created.

However, the final application is much more capable than that. The entire learning
-testing process, the backend and the clients are designed to provide a solution to any
image recognition problem. The steps in the teaching process were created from wellseparable, independent, and reusable components, and the functionality of the backend
and the clients is completely independent of the specific problem.

As a result of my work I managed to lay down a base for a universal, deep convolutional neural network-based
application, and a backend and clients for this application, that can help to solve any
image processing problem. I also illustrated the work of the application by teaching it on
vehicle categorization to prove the results and usability.

***
# About this program

The main goal of this client was to show the people that it's possible to use other clients than the normal ones. (web, phone etc.) I choosed the facebook messenger platform, and I created a simple "chatbot" to illustrate that my program can also work in this enviroment.

Using this platform is really easy, all you have to do is implement a webhook. The only problem is that you will need SSL, so I did this small "forwarding server" which can format, validate & forward the requests to my real backend. I deployed it to Heroku, you can see it works: [here (wait a few sec)](https://carrecognizer-messengerbot.herokuapp.com/check)

***
# Images
#### It's working
![It's working](https://github.com/banda13/Carrecongnizer-chatbot/blob/master/messenger-test.jpg)


***
# Links
## Other parts of the project
* [Carrecognizer main program, building & training convolutional networks, webcrawelers implementation & lot of other scripts and experiment results](https://github.com/banda13/Carrecognizer)
* [Preclassification convolutional modell determine valid vehicle images](https://github.com/banda13/Carrecognizer-preclassifier)
* [Database](https://github.com/banda13/Carrecognizer-database)
* [Django backend](https://github.com/banda13/Carrecognizer-backend)
* [Angular web application](https://github.com/banda13/Carrecognizer-angular)
* [Android application](https://github.com/banda13/Carrecognizer-android)
* [Messenger chatbot](https://github.com/banda13/Carrecongnizer-chatbot)
## Demos
* [Android client](https://www.youtube.com/watch?v=MohFNK0EPZ8)
* [Angular client](https://www.youtube.com/watch?v=G77Rl3K1amk)
## Thesis
* [Thesis](https://diplomaterv.vik.bme.hu/en/Theses/Gepjarmu-kategorizalas-konvolucios-neuralis)

_I hope you enjoy it (as much as I did) and I hope it can help a little bit to you! <3_
