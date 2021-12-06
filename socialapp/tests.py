'''
this file we create the test which is used to test our functions 
'''
from django.test import TestCase
from socialapp.forms import *
from socialapp.models import *
import uuid
from django.utils import timezone

# Create your tests here.
class AuthorTestCase(TestCase):

	def setUp(self):

		self.user_id_1 = uuid.uuid4()
		self.user_id_2 = uuid.uuid4()
		self.post_1 = uuid.uuid4()
		self.post_2 = uuid.uuid4()
		self.comment_1_id = uuid.uuid4()
		self.comment_2_id = uuid.uuid4()

		test_author_1 = Author()
		test_author_1.id = self.user_id_1
		test_author_1.displayName = "LIU"
		test_author_1.password = "12345"
		test_author_1.save()

		test_author_2 = Author()
		test_author_2.id = self.user_id_2
		test_author_2.displayName = "Zhang"
		test_author_2.password = "yyyyyyyy"
		test_author_2.save()

		test_post_1 = Post()
		test_post_1.id = self.post_1
		test_post_1.title = "This is the title of post 1"
		test_post_1.description = "This is the description of post 1"
		test_post_1.content = "This is the content of post 1"
		test_post_1.author = test_author_1
		test_post_1.visibility = "PUBLIC"
		test_post_1.unlisted = True
		test_post_1.contentType = "PLAIN"
		test_post_1.save()

		test_post_2 = Post()
		test_post_2.id = self.post_2
		test_post_2.title = "This is the title of post 2"
		test_post_2.description = "This is the description of post 2"
		test_post_2.content = "This is the content of post 2"
		test_post_2.author = test_author_2
		test_post_2.visibility = "PRIVATE"
		test_post_2.unlisted = False
		test_post_2.contentType = "PLAIN"
		test_post_2.save()

	def test_author(self):
		author_1 = Author.objects.get(pk=self.user_id_1)
		author_2 = Author.objects.get(pk=self.user_id_2)

		self.assertEqual(author_1.displayName, "LIU")
		self.assertEqual(author_1.password, "12345")

		self.assertEqual(author_2.displayName, "Zhang")
		self.assertEqual(author_2.password, "yyyyyyyy")


	def test_post(self):
		post_one = Post.objects.get(pk=self.post_1)
		post_two = Post.objects.get(pk=self.post_2)

		self.assertEqual(post_one.title, "This is the title of post 1")
		self.assertEqual(post_one.description, "This is the description of post 1")
		self.assertEqual(post_one.content, "This is the content of post 1")
		self.assertEqual(post_one.visibility, "PUBLIC")
		self.assertEqual(post_one.unlisted, True)
		self.assertEqual(post_one.contentType, "PLAIN")

		self.assertEqual(post_two.title, "This is the title of post 2")
		self.assertEqual(post_two.description, "This is the description of post 2")
		self.assertEqual(post_two.content, "This is the content of post 2")
		self.assertEqual(post_two.visibility, "PRIVATE")
		self.assertEqual(post_two.unlisted, False)
		self.assertEqual(post_two.contentType, "PLAIN")

	def test_edit_author(self):
		author_1 = Author.objects.get(pk=self.user_id_1)
		author_2 = Author.objects.get(pk=self.user_id_2)

		author_1.password = "54321"
		author_2.password = "wwwww"

		author_1.displayName = "car"
		author_2.displayName = "bicycle"

		self.assertEqual(author_1.displayName, "car")
		self.assertEqual(author_1.password, "54321")

		self.assertEqual(author_2.displayName, "bicycle")
		self.assertEqual(author_2.password, "wwwww")

	def test_edit_post(self):
		post_one = Post.objects.get(pk=self.post_1)
		post_two = Post.objects.get(pk=self.post_2)

		post_one.title = "1"
		post_one.description = "12"
		post_one.content = "123"
		post_one.visibility = "PRIVATE"
		post_one.unlisted = False
		post_one.contentType = "PLAIN"
		post_one.save()

		post_two.title = "3"
		post_two.description = "32"
		post_two.content = "321"
		post_two.visibility = "PRIVATE"
		post_two.unlisted = True
		post_two.contentType = "PLAIN"
		post_two.save()

		self.assertEqual(post_one.title, "1")
		self.assertEqual(post_one.description, "12")
		self.assertEqual(post_one.content, "123")
		self.assertEqual(post_one.visibility, "PRIVATE")
		self.assertEqual(post_one.unlisted, False)
		self.assertEqual(post_one.contentType, "PLAIN")

		self.assertEqual(post_two.title, "3")
		self.assertEqual(post_two.description, "32")
		self.assertEqual(post_two.content, "321")
		self.assertEqual(post_two.visibility, "PRIVATE")
		self.assertEqual(post_two.unlisted, True)
		self.assertEqual(post_two.contentType, "PLAIN")

	def test_Post_Like(self):
		Like.objects.create(object=Post.objects.get(id=self.post_1), author=Author.objects.get(id=self.user_id_1))
		post_like = Like.objects.all()
		self.assertEqual(len(post_like), 1)
		self.assertEqual(post_like.get().object.id, self.post_1)
		self.assertEqual(post_like.get().author.id, self.user_id_1)

	def test_Post_Like_Two(self):
		Like.objects.create(object=Post.objects.get(id=self.post_1), author=Author.objects.get(id=self.user_id_2))
		post_like = Like.objects.all()
		self.assertEqual(len(post_like), 1)
		self.assertEqual(post_like.get().object.id, self.post_1)
		self.assertEqual(post_like.get().author.id, self.user_id_2)

	def test_Post_Comment(self):
		Comment.objects.create(id=self.comment_1_id,post=Post.objects.get(id=self.post_1), author=Author.objects.get(id=self.user_id_1), comment="test for comment_1")
		post_comment = Comment.objects.get(id=self.comment_1_id)
		self.assertEqual(post_comment.comment, "test for comment_1")
		self.assertEqual(post_comment.id, self.comment_1_id)
		self.assertEqual(post_comment.author, Author.objects.get(id=self.user_id_1))

	def test_Post_Comment_Two(self):
		Comment.objects.create(id=self.comment_2_id,post=Post.objects.get(id=self.post_2), author=Author.objects.get(id=self.user_id_2), comment="test for comment_2")
		post_comment = Comment.objects.get(id=self.comment_2_id)
		self.assertEqual(post_comment.comment, "test for comment_2")
		self.assertEqual(post_comment.id, self.comment_2_id)
		self.assertEqual(post_comment.author, Author.objects.get(id=self.user_id_2))

# # Create your tests here.
# class AuthorTestCase(TestCase):

# 	def setUp(self):

# 		self.user_id_1 = uuid.uuid4()
# 		self.user_id_2 = uuid.uuid4()
# 		self.post_1 = uuid.uuid4()
# 		self.post_2 = uuid.uuid4()

# 		test_author_1 = Author()
# 		test_author_1.id = self.user_id_1
# 		test_author_1.displayName = "LIU"
# 		test_author_1.password = "12345"
# 		test_author_1.save()

# 		test_author_2 = Author()
# 		test_author_2.id = self.user_id_2
# 		test_author_2.displayName = "Zhang"
# 		test_author_2.password = "yyyyyyyy"
# 		test_author_2.save()

# 		test_post_1 = Post()
# 		test_post_1.id = self.post_1
# 		test_post_1.title = "This is the title of post 1"
# 		test_post_1.description = "This is the description of post 1"
# 		test_post_1.content = "This is the content of post 1"
# 		test_post_1.author = test_author_1
# 		test_post_1.visibility = "PUBLIC"
# 		test_post_1.unlisted = True
# 		test_post_1.contentType = "PLAIN"
# 		test_post_1.save()

# 		test_post_2 = Post()
# 		test_post_2.id = self.post_2
# 		test_post_2.title = "This is the title of post 2"
# 		test_post_2.description = "This is the description of post 2"
# 		test_post_2.content = "This is the content of post 2"
# 		test_post_2.author = test_author_2
# 		test_post_2.visibility = "PRIVATE"
# 		test_post_2.unlisted = False
# 		test_post_2.contentType = "PLAIN"
# 		test_post_2.save()

# 	def test_author(self):
# 		author_1 = Author.objects.get(pk=self.user_id_1)
# 		author_2 = Author.objects.get(pk=self.user_id_2)

# 		self.assertEqual(author_1.displayName, "LIU")
# 		self.assertEqual(author_1.password, "12345")

# 		self.assertEqual(author_2.displayName, "Zhang")
# 		self.assertEqual(author_2.password, "yyyyyyyy")


# 	def test_post(self):
# 		post_one = Post.objects.get(pk=self.post_1)
# 		post_two = Post.objects.get(pk=self.post_2)

# 		self.assertEqual(post_one.title, "This is the title of post 1")
# 		self.assertEqual(post_one.description, "This is the description of post 1")
# 		self.assertEqual(post_one.content, "This is the content of post 1")
# 		self.assertEqual(post_one.visibility, "PUBLIC")
# 		self.assertEqual(post_one.unlisted, True)
# 		self.assertEqual(post_one.contentType, "PLAIN")

# 		self.assertEqual(post_two.title, "This is the title of post 2")
# 		self.assertEqual(post_two.description, "This is the description of post 2")
# 		self.assertEqual(post_two.content, "This is the content of post 2")
# 		self.assertEqual(post_two.visibility, "PRIVATE")
# 		self.assertEqual(post_two.unlisted, False)
# 		self.assertEqual(post_two.contentType, "PLAIN")

# 	def test_edit_author(self):
# 		author_1 = Author.objects.get(pk=self.user_id_1)
# 		author_2 = Author.objects.get(pk=self.user_id_2)

# 		author_1.password = "54321"
# 		author_2.password = "wwwww"

# 		author_1.displayName = "car"
# 		author_2.displayName = "bicycle"

# 		self.assertEqual(author_1.displayName, "car")
# 		self.assertEqual(author_1.password, "54321")

# 		self.assertEqual(author_2.displayName, "bicycle")
# 		self.assertEqual(author_2.password, "wwwww")

# 	def test_edit_post(self):
# 		post_one = Post.objects.get(pk=self.post_1)
# 		post_two = Post.objects.get(pk=self.post_2)

# 		post_one.title = "1"
# 		post_one.description = "12"
# 		post_one.content = "123"
# 		post_one.visibility = "PRIVATE"
# 		post_one.unlisted = False
# 		post_one.contentType = "PLAIN"
# 		post_one.save()

# 		post_two.title = "3"
# 		post_two.description = "32"
# 		post_two.content = "321"
# 		post_two.visibility = "PRIVATE"
# 		post_two.unlisted = True
# 		post_two.contentType = "PLAIN"
# 		post_two.save()

# 		self.assertEqual(post_one.title, "1")
# 		self.assertEqual(post_one.description, "12")
# 		self.assertEqual(post_one.content, "123")
# 		self.assertEqual(post_one.visibility, "PRIVATE")
# 		self.assertEqual(post_one.unlisted, False)
# 		self.assertEqual(post_one.contentType, "PLAIN")

# 		self.assertEqual(post_two.title, "3")
# 		self.assertEqual(post_two.description, "32")
# 		self.assertEqual(post_two.content, "321")
# 		self.assertEqual(post_two.visibility, "PRIVATE")
# 		self.assertEqual(post_two.unlisted, True)
# 		self.assertEqual(post_two.contentType, "PLAIN")


