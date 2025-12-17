'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useForm } from 'react-hook-form';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card, CardBody } from '@/components/ui/Card';
import { authService } from '@/lib/auth.service';
import { RegisterData } from '@/lib/types';
import toast from 'react-hot-toast';

export default function RegisterPage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const { register, handleSubmit, watch, formState: { errors } } = useForm<RegisterData>();
  const password = watch('password');

  const onSubmit = async (data: RegisterData) => {
    setIsLoading(true);
    try {
      await authService.register(data);
      toast.success('Registration successful! Please login.');
      router.push('/login');
    } catch (error: any) {
      const errorMsg = error.response?.data;
      if (typeof errorMsg === 'object') {
        Object.keys(errorMsg).forEach(key => {
          toast.error(`${key}: ${errorMsg[key]}`);
        });
      } else {
        toast.error('Registration failed. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center px-4 py-12 bg-gray-50">
      <Card className="w-full max-w-2xl">
        <CardBody className="p-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Create Account</h1>
            <p className="text-gray-600">Join LibraryHub today</p>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Input
                label="Username"
                type="text"
                placeholder="Choose a username"
                error={errors.username?.message}
                {...register('username', { required: 'Username is required' })}
              />

              <Input
                label="Email"
                type="email"
                placeholder="your@email.com"
                error={errors.email?.message}
                {...register('email', {
                  required: 'Email is required',
                  pattern: {
                    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                    message: 'Invalid email address',
                  },
                })}
              />

              <Input
                label="First Name"
                type="text"
                placeholder="First name"
                error={errors.first_name?.message}
                {...register('first_name', { required: 'First name is required' })}
              />

              <Input
                label="Last Name"
                type="text"
                placeholder="Last name"
                error={errors.last_name?.message}
                {...register('last_name', { required: 'Last name is required' })}
              />

              <Input
                label="Phone Number (Optional)"
                type="tel"
                placeholder="+1234567890"
                error={errors.phone_number?.message}
                {...register('phone_number')}
              />

              <Input
                label="Address (Optional)"
                type="text"
                placeholder="Your address"
                error={errors.address?.message}
                {...register('address')}
              />

              <Input
                label="Password"
                type="password"
                placeholder="Create a password"
                error={errors.password?.message}
                {...register('password', {
                  required: 'Password is required',
                  minLength: {
                    value: 8,
                    message: 'Password must be at least 8 characters',
                  },
                })}
              />

              <Input
                label="Confirm Password"
                type="password"
                placeholder="Confirm your password"
                error={errors.password2?.message}
                {...register('password2', {
                  required: 'Please confirm your password',
                  validate: (value) => value === password || 'Passwords do not match',
                })}
              />
            </div>

            <Button
              type="submit"
              className="w-full"
              isLoading={isLoading}
            >
              Create Account
            </Button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-gray-600">
              Already have an account?{' '}
              <Link href="/login" className="text-primary-600 hover:text-primary-700 font-medium">
                Sign in
              </Link>
            </p>
          </div>
        </CardBody>
      </Card>
    </div>
  );
}
