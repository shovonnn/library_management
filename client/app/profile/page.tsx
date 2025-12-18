'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { useAuthStore } from '@/lib/store';
import { authService } from '@/lib/auth.service';
import { Card, CardBody, CardHeader } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';
import { LoadingPage } from '@/components/ui/Loading';
import { User, Mail, Phone, MapPin, Shield } from 'lucide-react';
import toast from 'react-hot-toast';

interface ProfileForm {
  first_name: string;
  last_name: string;
  email: string;
  phone_number?: string;
  address?: string;
}

interface PasswordForm {
  old_password: string;
  new_password: string;
  new_password2: string;
}

export default function ProfilePage() {
  const router = useRouter();
  const { user, isAuthenticated, isLoading: authLoading, fetchUser } = useAuthStore();
  const [isUpdating, setIsUpdating] = useState(false);
  const [isChangingPassword, setIsChangingPassword] = useState(false);

  const { register, handleSubmit, formState: { errors }, reset } = useForm<ProfileForm>();
  const { register: registerPassword, handleSubmit: handleSubmitPassword, watch, formState: { errors: passwordErrors }, reset: resetPassword } = useForm<PasswordForm>();

  const newPassword = watch('new_password');

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
      return;
    }

    if (user) {
      reset({
        first_name: user.first_name,
        last_name: user.last_name,
        email: user.email,
        phone_number: user.phone_number,
        address: user.address,
      });
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user, isAuthenticated, authLoading, reset]);

  const onSubmitProfile = async (data: ProfileForm) => {
    setIsUpdating(true);
    try {
      await authService.updateProfile(data);
      await fetchUser();
      toast.success('Profile updated successfully');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to update profile');
    } finally {
      setIsUpdating(false);
    }
  };

  const onSubmitPassword = async (data: PasswordForm) => {
    setIsChangingPassword(true);
    try {
      await authService.changePassword(data.old_password, data.new_password);
      toast.success('Password changed successfully');
      resetPassword();
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to change password');
    } finally {
      setIsChangingPassword(false);
    }
  };

  if (authLoading || !user) {
    return <LoadingPage />;
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">My Profile</h1>
        <p className="text-lg text-gray-600">Manage your account information</p>
      </div>

      <div className="space-y-6">
        {/* Account Info */}
        <Card>
          <CardHeader>
            <div className="flex items-center space-x-2">
              <User className="h-5 w-5 text-primary-600" />
              <h2 className="text-xl font-semibold">Account Information</h2>
            </div>
          </CardHeader>
          <CardBody>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-600">Username</p>
                <p className="font-medium">{user.username}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Role</p>
                <span className={`inline-block px-3 py-1 rounded-full text-xs font-semibold ${
                  user.role === 'admin' ? 'bg-purple-100 text-purple-800' : 'bg-blue-100 text-blue-800'
                }`}>
                  {user.role.toUpperCase()}
                </span>
              </div>
              <div>
                <p className="text-sm text-gray-600">Member Since</p>
                <p className="font-medium">{new Date(user.date_joined).toLocaleDateString()}</p>
              </div>
            </div>
          </CardBody>
        </Card>

        {/* Profile Form */}
        <Card>
          <CardHeader>
            <h2 className="text-xl font-semibold">Personal Information</h2>
          </CardHeader>
          <CardBody>
            <form onSubmit={handleSubmit(onSubmitProfile)} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Input
                  label="First Name"
                  type="text"
                  error={errors.first_name?.message}
                  {...register('first_name', { required: 'First name is required' })}
                />
                <Input
                  label="Last Name"
                  type="text"
                  error={errors.last_name?.message}
                  {...register('last_name', { required: 'Last name is required' })}
                />
                <Input
                  label="Email"
                  type="email"
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
                  label="Phone Number"
                  type="tel"
                  error={errors.phone_number?.message}
                  {...register('phone_number')}
                />
              </div>
              <Input
                label="Address"
                type="text"
                error={errors.address?.message}
                {...register('address')}
              />
              <Button type="submit" isLoading={isUpdating}>
                Update Profile
              </Button>
            </form>
          </CardBody>
        </Card>

        {/* Change Password */}
        <Card>
          <CardHeader>
            <div className="flex items-center space-x-2">
              <Shield className="h-5 w-5 text-primary-600" />
              <h2 className="text-xl font-semibold">Change Password</h2>
            </div>
          </CardHeader>
          <CardBody>
            <form onSubmit={handleSubmitPassword(onSubmitPassword)} className="space-y-4">
              <Input
                label="Current Password"
                type="password"
                error={passwordErrors.old_password?.message}
                {...registerPassword('old_password', { required: 'Current password is required' })}
              />
              <Input
                label="New Password"
                type="password"
                error={passwordErrors.new_password?.message}
                {...registerPassword('new_password', {
                  required: 'New password is required',
                  minLength: {
                    value: 8,
                    message: 'Password must be at least 8 characters',
                  },
                })}
              />
              <Input
                label="Confirm New Password"
                type="password"
                error={passwordErrors.new_password2?.message}
                {...registerPassword('new_password2', {
                  required: 'Please confirm your password',
                  validate: (value) => value === newPassword || 'Passwords do not match',
                })}
              />
              <Button type="submit" isLoading={isChangingPassword}>
                Change Password
              </Button>
            </form>
          </CardBody>
        </Card>
      </div>
    </div>
  );
}
