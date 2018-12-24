import tensorflow as tf
import numpy as np

n_inputs = 3

n_neuros = 5

n_steps = 2

seq_length = tf.placeholder(tf.int32, [None])

X = tf.placeholder(tf.float32, [None, n_steps, n_inputs])

X_seqs = tf.unstack(tf.transpose(X, perm=[1, 0, 2]))

basic_cell = tf.contrib.rnn.BasicRNNCell(num_units=n_neuros)

output_seqs, states = tf.contrib.rnn.static_rnn(basic_cell, X_seqs, dtype=tf.float32, sequence_length=seq_length)

outputs = tf.transpose(tf.stack(output_seqs), perm=[1,0,2])

X_batch = np.random.rand(4, 2, 3)

seq_leng_batch = np.array([2, 2, 2, 2])

with tf.Session() as sess:
    tf.global_variables_initializer().run()
    outputs_val, states_val = sess.run([outputs, states], feed_dict={X:X_batch, seq_length:seq_leng_batch})
    outputs_val1, states_val1 = sess.run([outputs, states], feed_dict={X:X_batch, seq_length:seq_leng_batch})
    assert(np.all(outputs_val==outputs_val1))
    seq_leng_batch = np.array([2, 2, 2, 2])
    outputs_val2, states_val2 = sess.run([outputs, states], feed_dict={X:X_batch, seq_length:seq_leng_batch})
