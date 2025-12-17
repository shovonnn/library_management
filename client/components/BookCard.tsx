import React from 'react';
import { Book } from '@/lib/types';
import { Card, CardBody } from './ui/Card';
import { Button } from './ui/Button';
import { BookOpen, User as UserIcon } from 'lucide-react';
import { truncate } from '@/lib/utils';

interface BookCardProps {
  book: Book;
  onBorrow?: (book: Book) => void;
  onView?: (book: Book) => void;
  isLoading?: boolean;
}

export const BookCard: React.FC<BookCardProps> = ({
  book,
  onBorrow,
  onView,
  isLoading,
}) => {
  return (
    <Card hover className="h-full flex flex-col">
      <div className="relative h-64 bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center">
        {book.cover_image ? (
          <img
            src={book.cover_image}
            alt={book.title}
            className="h-full w-full object-cover"
          />
        ) : (
          <BookOpen className="h-24 w-24 text-white opacity-50" />
        )}
        {!book.is_available && (
          <div className="absolute top-2 right-2 bg-red-600 text-white px-3 py-1 rounded-full text-xs font-semibold">
            Unavailable
          </div>
        )}
        {book.is_available && (
          <div className="absolute top-2 right-2 bg-green-600 text-white px-3 py-1 rounded-full text-xs font-semibold">
            Available
          </div>
        )}
      </div>
      
      <CardBody className="flex-1 flex flex-col">
        <div className="flex-1">
          <h3 className="text-lg font-bold text-gray-900 mb-2">
            {truncate(book.title, 50)}
          </h3>
          <div className="flex items-center text-gray-600 mb-2">
            <UserIcon className="h-4 w-4 mr-1" />
            <span className="text-sm">{book.author}</span>
          </div>
          <p className="text-sm text-gray-600 mb-2">
            Category: <span className="font-medium">{book.category}</span>
          </p>
          {book.description && (
            <p className="text-sm text-gray-600 mb-4">
              {truncate(book.description, 100)}
            </p>
          )}
          <div className="flex justify-between text-sm text-gray-600">
            <span>Available: {book.available_copies}/{book.total_copies}</span>
            <span>Pages: {book.page_count}</span>
          </div>
        </div>
        
        <div className="mt-4 flex space-x-2">
          {onView && (
            <Button
              variant="ghost"
              size="sm"
              className="flex-1"
              onClick={() => onView(book)}
            >
              View Details
            </Button>
          )}
          {onBorrow && book.is_available && (
            <Button
              variant="primary"
              size="sm"
              className="flex-1"
              onClick={() => onBorrow(book)}
              isLoading={isLoading}
            >
              Borrow
            </Button>
          )}
        </div>
      </CardBody>
    </Card>
  );
};
