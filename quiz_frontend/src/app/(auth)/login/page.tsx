"use client"

import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import Button from '@/components/layout/Button';
import { FormType } from '@/lib/utils/types';
import Link from 'next/link';
import { setCookie } from 'cookies-next';
import { useRouter } from 'next/navigation';

const page = () => {

  // let [formData, setFormData] = useState(new FormData())

  const [error, setError] = useState<string>();
  const { register, handleSubmit } = useForm<FormType>();
  const router = useRouter();

  const loginFn = async (data: FormType) => {
    const response = await fetch(`/api/api/Signin`,
      {
        method: "POST",
        headers: {
          "content-type": "application/json"
        },
        body: JSON.stringify(data)
      }
    );
    if (!response.ok) {
      setError(await response.json());
    } else {
      setError("");
      console.log(await response.json());
      
      // const { access_token, refresh_token } = await response.json();

      // const access_exipration_time = new Date();
      // access_exipration_time.setSeconds(access_exipration_time.getSeconds() + access_token.access_expiry_time);

      // const refresh_exipration_time = new Date();
      // refresh_exipration_time.setSeconds(refresh_exipration_time.getSeconds() + refresh_token.refresh_expiry_time);

      // setCookie("access_token", access_token.token, {
      //   expires: access_exipration_time,
      //   secure: true
      // });

      // setCookie("refresh_token", refresh_token.token, {
      //   expires: refresh_exipration_time,
      //   secure: true
      // });

      router.push("/")
    }
  };
  return (
    <main className='h-screen flex justify-center items-center bg-gradient-to-tr from-black via-slate-950 to-blue-950'>

      <div className='w-1/3 p-6 rounded-md bg-white flex flex-col gap-2 justify-center items-center'>
        <h1 className='md:text-2xl text-xl font-bold text-gray-900 m-2'>Welcome to Quiz Hub</h1>
        <p className='text-red-500'>{error ? error : ""}</p>
        <form onSubmit={handleSubmit(loginFn)} className='flex flex-col gap-4 justify-center items-center'>
          {/* 
          <input className='rounded-md border  p-1.5' type="text" placeholder='userName'  {...register("user_name", {
            required: true,
            // pattern:"^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$"
          })} /> */}

          <input className='rounded-md border p-1.5' type="email" placeholder='userEmail' {...register("user_email", {
            required: true
          })} />
          <input className='rounded-md border p-1.5' type="password" placeholder='userPassword' {...register("user_password", {
            required: true,
            minLength: 6
          })} />
          <Button buttonType='submit'>
            Sign In
          </Button>
        </form>

        <h1 className='md:text-xl text-gray-900 m-2'>
          Don't have an account?
        </h1>
        <Link href={"/register"}>
          <Button buttonType='button'>
            Sign Up
          </Button>
        </Link>
      </div>
    </main>
  )
}

export default page


//  How register works?

// {
//   user_name:"bilal"
// }
// {
//   user_name:"bilal",
//   user_email: "bilal2gmil.vom"
// }
// {
//   user_name:"bilal",
//   user_email: "bilal2gmil.vom",
//   user_password:"bilal123"
// }

// destructuring in javascript

// const {access_token, refresh_token} = {
//   access_token: {

//   },
//   refresh_token: {

//   }
// }