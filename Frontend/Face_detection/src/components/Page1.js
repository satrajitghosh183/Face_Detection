import React from 'react'
import download from '../images/download.jpeg';
import facial from '../images/facial-recognition-data-collection.jpg'
import axios from "axios";
// import txt1 from '../text/text1.txt'
import { Link } from 'react-router-dom'

const Page1 = () => {
  const submit = async(e)=>{

    e.preventDefault();
    try{
      await axios.get('http://127.0.0.1:5000');
      console.log('success');
    }catch(e){
      console.log(e);
    }
    
  }
  return (
    // <main class='bg-blue-200 w-10'></main>
    <>
       <main class='bg-slate-50 px-36 mx-48 my-45 rounded-2xl justify-between  mt-28 h-screen place-items-center py-10 dark:bg-slate-800 text-gray-50 flex-auto space-y-16 shadow-2xl'>
           <h1 class='justify-self-center text-amber-400 text-4xl mb-14 ml-64'>Face Detection</h1>
           <h2 class='font-serif'>Welcome to our website, where we present our state-of-the-art face recognition algorithm. We have leveraged the power of OpenCV MediaPipe to develop an advanced algorithm that can accurately recognize faces in real-time. Our algorithm is designed to work seamlessly with a MongoDB database, which allows for efficient storage and retrieval of face data. To provide an intuitive user interface, we have integrated our algorithm with a ReactJS frontend that offers a user-friendly experience.</h2>
           <img class='w-10/12 ml-14 mb-7' src={facial}></img>
       </main>
       <div class='justify-self-end'>
            <h1 class='font-bold text-4xl mb-10 mt-28 ml-36'>Information
              </h1>
            <div class='mx-36 font-serif'>Our system is designed to address the increasing demand for reliable face detection systems that can function effectively in complex and changing environments.<br></br><br></br>
            At the heart of our system are two powerful computer vision libraries - OpenCV and MediaPipe. OpenCV provides a variety of pre-trained models, including Haar Cascades and Deep Learning-based models, that are optimized for speed and accuracy. MediaPipe offers a pipeline-based architecture that optimizes the processing of data, making it suitable for real-time applications. By integrating these two libraries, we have created an advanced algorithm that is capable of detecting faces in real-time with high accuracy.<br></br><br></br>
            To enable efficient storage and retrieval of face data, we have integrated our system with a MongoDB database. MongoDB is a NoSQL database that is designed for scalability and flexibility. It can handle large amounts of data effectively, making it an excellent choice for storing and retrieving face data. With this integration, our system can store and retrieve face data efficiently, allowing for fast and reliable access to the data.<br></br><br></br>
            The ReactJS frontend provides an intuitive user interface for interacting with the system, making it easy to visualize and analyze the data. The user-friendly interface allows users to interact with the system effectively and provides a platform for analysis of the data.<br></br><br></br>
            Our face detection system is suitable for various applications, including security, surveillance, and user experience. For example, it can be used in security systems to monitor the entry and exit of individuals in a restricted area, or in user experience systems to enhance facial recognition in smart homes, automobiles, and other devices. Our solution is likely to find widespread adoption in these fields due to its high accuracy, efficiency, and user-friendliness.<br></br><br></br>
            Explore our website to learn more about our technology and how it can benefit your work. We offer a powerful, reliable, and advanced solution that can meet your face detection needs.

          </div>
       </div>

<div class= 'my-16'>
  {/* <button class='bg-neutral-800 text-gray-50 px-2 py-2 rounded-lg w-20 ml-24' disabled='true'>prev</button> */}
  <Link to={'/page2'}><button class='bg-neutral-800 text-gray-50 px-2 py-2 rounded-lg w-72 h-11 ml-36' onClick={submit}>start</button></Link>
</div>
       
    </>
  )
}

export default Page1